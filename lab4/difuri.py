import pylab as pp
import numpy as np
from scipy import integrate, optimize
from scipy.integrate import odeint

class ParameterEstimator:
    def __init__(self, x_data, y_data, f):
        self._x_data = x_data
        self._y_data = y_data
        self._f = f
        self._c = None
        self.n_observed = y_data.shape[1]

    def estimate(self, y0, guess):
        self._y0_len = len(y0)
        self._est_values = np.concatenate((y0, guess))
        (c, _) = optimize.leastsq(self.f_resid, self._est_values)
        self._c = c
        return c[self._y0_len:], c[0:self._y0_len]

    def f_resid(self, p):
        delta = self._y_data - self.my_ls_func(self._x_data, p)
        return delta.flatten()

    def my_ls_func(self, x, teta):
        r = integrate.odeint(lambda y, t: self._f(y, t, teta[self._y0_len:]),
                             teta[0:self._y0_len], x)
        return r[:, 0:self.n_observed]

    def plot_result(self):
        if self._c is None:
            print("Параметры не оценены.")
            return
        sol, t = self.calcODE((self._c[self._y0_len:],),
                              self._c[0:self._y0_len],
                              min(self._x_data), max(self._x_data))
        pp.plot(self._x_data, self._y_data, '.r', t, sol[:, 0], '-b')
        pp.xlabel('Время')
        pp.ylabel('y(t)')
        pp.legend(('Данные', 'Модель'), loc='best')
        pp.show()

    def calcODE(self, args, y0, x0=0, xEnd=10, nt=101):
        t = np.linspace(x0, xEnd, nt)
        sol = odeint(self._f, y0, t, args)
        return sol, t

def ode(y, t, k):
    x1, x2 = y
    a, b = k
    u = 1
    return [x2, -a * x2 - b * x1 + 3 * u]

def calcODE(args, y0, ts=10, nt=101):
    t = np.linspace(0, ts, nt)
    sol = odeint(ode, y0, t, args)
    return sol, t

true_a, true_b = 2, 2
args = ([true_a, true_b],)
y0 = [0, 0]
sol, t = calcODE(args, y0, ts=10, nt=101)
y_data = sol[:, 0].reshape(-1, 1)

estimator = ParameterEstimator(t, y_data, ode)
est_par, est_y0 = estimator.estimate(y0=[0, 0], guess=[1.5, 1.5])

print(f"Истинные параметры: a={true_a}, b={true_b}")
print(f"Оцененные параметры: a={est_par[0]:.2f}, b={est_par[1]:.2f}")
print(f"Оцененные начальные условия: {est_y0}")

estimator.plot_result()