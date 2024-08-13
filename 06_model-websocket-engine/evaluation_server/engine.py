"""
Provides a solving engine for systems of sympy equations
"""

from __future__ import annotations
import struct
from typing import Callable, Iterator


import numpy
from numpy import ndarray
from sympy import Expr, Symbol, diff, Matrix, parse_expr, pretty
from sympy.utilities.lambdify import lambdify


numpy.set_printoptions(suppress=True, formatter={"float": "{: 20.12f}".format})


class Model:

    independent_variables: tuple[Symbol, ...]
    dependent_variables: tuple[Symbol, ...]
    equations: Matrix
    jacobian: Matrix
    F: Callable[..., ndarray]
    J: Callable[..., ndarray]
    X: ndarray
    Y: ndarray
    converged: bool = False

    def __init__(
        self,
        independent_variables: tuple[Symbol, ...],
        dependent_variables: tuple[Symbol, ...],
        equations: Matrix,
        jacobian: Matrix,
        F: Callable[..., ndarray],
        J: Callable[..., ndarray],
        X: ndarray,
        Y: ndarray,
        converged: bool = False,
    ) -> None:
        self.independent_variables = independent_variables
        self.dependent_variables = dependent_variables
        self.equations = equations
        self.jacobian = jacobian
        self.F = F
        self.J = J
        self.X = X
        self.Y = Y
        self.converged = converged

    @property
    def solution(self) -> ndarray:
        """
        Gets the solution array
        """
        if self.converged:
            return self.Y

        return numpy.array([numpy.NaN for _ in self.dependent_variables])

    @property
    def packed_solution(self) -> bytes:
        """
        Solution packed into bytes
        """
        _sol = tuple(self.solution.flat)
        _fmt = "d" * len(_sol)
        return struct.pack(_fmt, *_sol)

    @classmethod
    def from_sympy(
        cls,
        eqns: tuple[Expr, ...],
        independent_variables: tuple[Symbol, ...],
        dependent_variables: tuple[Symbol, ...],
        X: ndarray = numpy.array([[1.0], [1.0], [1.0]]),
        Y: ndarray = numpy.array([[1.0], [1.0], [1.0]]),
    ) -> Model:
        """
        The build a model from a system of sympy equation
        """
        _equations = Matrix(eqns)
        _f = lambdify(
            args=(*independent_variables, *dependent_variables),
            expr=_equations,
            modules="numpy",
        )

        _jacobian = Matrix([[diff(f, y) for y in dependent_variables] for f in eqns])
        _grad = lambdify(
            args=(*independent_variables, *dependent_variables),
            expr=_jacobian,
            modules="numpy",
        )

        return cls(
            independent_variables=independent_variables,
            dependent_variables=dependent_variables,
            equations=_equations,
            jacobian=_jacobian,
            F=_f,
            J=_grad,
            X=X,
            Y=Y,
        )

    @classmethod
    def build_known_solution_example(cls) -> Model:
        """
        Builds an example model
            0 = 3 * X1 - cos(X2 * X3) - 0.5
            0 = X1 ** 2 - 81 * (X2 + 0.1) ** 2 + sin(X3) + 1.06
            0 = exp(-X1 * X2) + 20 * X3 + Y1 * (10 * pi - 3) / 3

        Xi = [0.1, 0.1, -0.1]

        With a known solution
            x1 = 0.5
            x2 = 0.0
            x3 = -0.5235987756
        """

        dep_var = (Symbol("X1"), Symbol("X2"), Symbol("X3"))
        ind_var = ()
        _X = numpy.array([])
        symbols = {str(i): i for i in (*dep_var, *ind_var)}
        _eqns = (
            parse_expr("3 * X1 - cos(X2 * X3) - 0.5", symbols),
            parse_expr("X1 ** 2 - 81 * (X2 + 0.1) ** 2 + sin(X3) + 1.06", symbols),
            parse_expr("exp(-X1 * X2) + 20 * X3 + (10 * pi - 3) / 3", symbols),
        )
        _Y = numpy.array([[0.1], [0.1], [-0.1]])

        return Model.from_sympy(
            eqns=_eqns,
            independent_variables=ind_var,
            dependent_variables=dep_var,
            X=_X,
            Y=_Y,
        )

    @classmethod
    def build_example(cls) -> Model:
        """
        Builds an example model
                                Y1 * Y3 = 3 * X1 - cos(X2 * X3) - 0.5
                         Y2**2 - 3 * Y3 = X1 ** 2 - 81 * (X2 + 0.1) ** 2 + sin(X3) + 1.06
            Y3 - Y1 * (10 * pi - 3) / 3 = exp(-X1 * X2) + 20 * X3
        """

        dep_var = (Symbol("Y1"), Symbol("Y2"), Symbol("Y3"))
        ind_var = (Symbol("X1"), Symbol("X2"), Symbol("X3"))
        _X = numpy.array([[1.0], [1.0], [1.0]])
        symbols = {str(i): i for i in (*dep_var, *ind_var)}
        _eqns = (
            parse_expr("3 * X1 - cos(X2 * X3) - 0.5 - Y1 * Y3", symbols),
            parse_expr(
                "X1 ** 2 - 81 * (X2 + 0.1) ** 2 + sin(X3) + 1.06 - Y2**2 + 3 * Y3",
                symbols,
            ),
            parse_expr("exp(-X1 * X2) + 20 * X3 + (10 * pi - 3) / 3 - Y3", symbols),
        )
        _Y = numpy.array([[1.0], [1.0], [1.0]])

        return Model.from_sympy(
            eqns=_eqns,
            independent_variables=ind_var,
            dependent_variables=dep_var,
            X=_X,
            Y=_Y,
        )

    def to_pretty(self) -> str:
        """
        Prints the model equations and Jacobian
        """
        return f"Equations:\n{pretty(self.equations, use_unicode=False)}\n\nJacobian Matrix\n{pretty(self.jacobian, use_unicode=False)}\n"

    def convergence_iterator(
        self,
        independant_args=tuple[float, ...],
        tolerance: float = 10**-10,
        limit: int = 10_000,
    ) -> Iterator[str]:
        """
        Iterates until convergence tolerance or limit is reached. Yields a formated line of the output table after each
        iteration.
        """
        self.converged = False
        self.X = numpy.array([[i] for i in independant_args])
        k = 0

        header = "\n {: >5} [".format("k")
        header += " ".join(["{: >20}".format(str(i)) for i in self.dependent_variables])
        header += "] {: >20}".format("|| dy ||")
        header += "\n" + "=" * len(header) + "=\n"
        header += " {: >5} ".format(k) + str(self.Y[:, 0]) + " {:20}".format("")
        yield header

        for i in range(limit):
            k += 1
            Fk = self.F(*self.X.flat, *self.Y.flat)
            Jk = self.J(*self.X.flat, *self.Y.flat)
            dY = numpy.linalg.solve(Jk, -Fk)
            self.Y = self.Y + dY
            error = float(numpy.linalg.norm(dY))
            yield " {: >5} ".format(k) + str(self.Y[:, 0]) + " {: 20.12f}".format(error)
            if error < tolerance:
                self.converged = True
                break

        footer = "\n Result\n" + ("-" * 32) + "\n "
        footer += "\n ".join(
            [
                "{: >10} {: 20.12f}".format(str(v), y)
                for v, y in zip(self.dependent_variables, self.solution.flat)
            ]
        )
        footer += "\n {: >10} {:>20}".format("Converged", str(self.converged))
        yield footer


if __name__ == "__main__":

    model = Model.build_example()
    print(model.to_pretty())
    for log in model.convergence_iterator((0.1, 0.1, 0.1)):
        print(log)

    pretty(model.packed_solution)
