from flask import Flask, request, jsonify
from ortools.linear_solver import pywraplp

app = Flask(__name__)

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    # Example of a simple linear problem
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return jsonify({'error': 'Solver not created.'}), 500

    infinity = solver.infinity()
    x = solver.NumVar(0.0, infinity, 'x')
    y = solver.NumVar(0.0, infinity, 'y')

    # Define the constraints
    solver.Add(x + 2 * y <= 14)
    solver.Add(3 * x - y >= 0)
    solver.Add(x - y <= 2)

    # Define the objective function
    solver.Maximize(x + 10 * y)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        result = {
            'objective_value': solver.Objective().Value(),
            'x': x.solution_value(),
            'y': y.solution_value()
        }
        return jsonify(result)
    else:
        return jsonify({'error': 'No optimal solution found.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
