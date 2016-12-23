import pulp
import argparse
import sys
import json

def solve(objective=None, constraints=None, variables=None, lp_type=None):

    if lp_type == "max":
        lp_type = pulp.LpMaximize
    elif lp_type == "min":
        lp_type = pulp.LpMinimize

    simplex = pulp.LpProblem("Linear Programing", lp_type)

    for var in variables:
        exec(
            "{} = pulp.LpVariable('{}', lowBound=0, cat=pulp.LpInteger)".format(
                var, var)
        )

    for constraint in constraints:
        simplex += eval(constraint)

    simplex += eval(objective)

    try:
        results = simplex.solve()
        status = pulp.LpStatus[results]

        out = {
            'Status': status,
            'Variable And Solution': [{'name': var.name, 'value': var.value()} for var in simplex.variables()],
            'Z': simplex.objective.value(),
        }
    except Exception as e:
        out = {
            'error': True,
            'message': e.message,
        }

    return out


def execute():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', help='objective ')
    parser.add_argument('-c', help='constraints ', nargs='+')
    parser.add_argument('-v', help='variables', nargs='+')
    parser.add_argument('-t', help='min / max')
    args = parser.parse_args()

    if sys.argv[1] == '-h':
        parser.print_help()
    else:
        values = solve(
            objective=args.o,
            constraints=args.c,
            variables=args.v,
            lp_type=args.t
        )

        print(json.dumps(values, indent=4))

if __name__ == '__main__':
    execute()
