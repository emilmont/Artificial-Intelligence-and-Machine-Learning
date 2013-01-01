from copy import deepcopy
from cte import path, weight_data, weight_smooth, p_gain, d_gain


def twiddle(init_params, error_func, tol=0.01):
    n_params = len(init_params)
    p  = deepcopy(init_params)
    dp = [1.0] * n_params
    
    best_error = float("inf")
    n = 0
    while sum(dp) >= tol:
        for i in range(n_params):
            print '.',
            p[i] += dp[i]
            err = error_func(p)
            if err < best_error:
                best_error = err
                dp[i] *= 1.1
            else:
                p[i] -= 2.0 * dp[i]
                err = error_func(p)
                if err < best_error:
                    best_error = err
                    dp[i] * 1.1
                else:
                    p[i] += dp[i]
                    dp[i] *= 0.9
        n += 1
        print "\nTwiddle #", n, p, ' -> ', best_error, '(%.4f >= %.4f)' % (sum(dp), tol)
    return p


print twiddle([weight_data, weight_smooth, p_gain, d_gain], path.error)
