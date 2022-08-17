import spacetime as st
import numpy as np
import unittest

def check_boost_event_1D(v, event):
    t = event[0]
    x = event[1]
    L_factor = (1 - v ** 2) ** 0.5
    t_out = (t - v * x) / L_factor
    x_out = (x - v * t) / L_factor
    return np.array([t_out, x_out])

def check_boost_velocity_1D(v, u):
    v = np.array(v)
    u = np.array(u)
    return (u - v) / (1 - u * v)

class SpacetimeTestSuite(unittest.TestCase):

    # Test boosting events in one spatial dimension with randomized inputs
    def test_boost_event_1D_random(self):
        v_batch = []
        event_batch = []
        event_out_batch = []

        for _ in range(10):
            v = np.random.uniform(low=0.1, high=1.0, size=()).astype(np.double)
            event = np.random.uniform(low=-1000, high=1000, size=(2,)).astype(np.double)

            event_out = st.boost(v, event)

            event_out_check = check_boost_event_1D(v, event)
            assert np.isclose(event_out, event_out_check).all()

            v_batch.append(v)
            event_batch.append(event)
            event_out_batch.append(event_out)

        # Test batched mode
        v = np.array(v_batch, dtype=np.double)
        event = np.array(event_batch, dtype=np.double)
        event_out_check = np.array(event_out_batch, dtype=np.double)

        event_out = st.boost(v, event)

        assert np.isclose(event_out, event_out_check).all()

    # Test boosting velocities in one spatial dimension with randomized inputs
    def test_boost_velocity_1D_random(self):
        v_batch = []
        event_batch = []
        event_out_batch = []
        u_batch = []
        u_out_batch = []

        for _ in range(10):
            v = np.random.uniform(low=0.1, high=1.0, size=()).astype(np.double)
            u = np.random.uniform(low=0.1, high=1.0, size=()).astype(np.double)
            event = np.random.uniform(low=-1000, high=1000, size=(2,)).astype(np.double)

            event_out, u_out = st.boost(v, event, u)

            u_out_check = check_boost_velocity_1D(v, u)
            event_out_check = check_boost_event_1D(v, event)
            assert np.isclose(u_out, u_out_check).all()
            assert np.isclose(event_out, event_out_check).all()

            v_batch.append(v)
            event_batch.append(event)
            event_out_batch.append(event_out)
            u_batch.append(u)
            u_out_batch.append(u_out)

        # Test batched mode
        v = np.array(v_batch, dtype=np.double)
        event = np.array(event_batch, dtype=np.double)
        event_out_check = np.array(event_out_batch, dtype=np.double)
        u = np.array(u_batch, dtype=np.double)
        u_out_check = np.array(u_out_batch, dtype=np.double)

        event_out, u_out = st.boost(v, event, u)

        assert np.isclose(event_out, event_out_check).all()
        assert np.isclose(u_out, u_out_check).all()

    def test_Worldline_eval(self):
        w0 = st.Worldline(
            [[0, 0]],
            end_velocities=[[0.9], [0]])
        w1 = st.Worldline(
            [[0, 0], [1, 0.9], [2, 0], [4, 2]],
            end_velocities=[[-0.1], [0.9]])
        test_cases = [
            # worldline, time, event_check
            (w0, 0, [0, 0]),
            (w0, 1, [1, 0]),
            (w0, -1, [-1, -0.9]),
            (w1, 0, [0, 0]),
            (w1, 0.5, [0.5, 0.45]),
            (w1, 1, [1, 0.9]),
            (w1, 1.25, [1.25, 0.9 * 3 / 4]),
            (w1, 2, [2, 0]),
            (w1, 3, [3, 1]),
            (w1, 5, [5, 2 + 0.9]),
            (w1, 50, [50, 2 + 0.9 * 46]),
            (w1, -1, [-1, 0.1]),
            (w1, -100, [-100, 10]),
        ]
        for w, t, event_check in test_cases:
            assert event_check[0] == t, 'test case is invalid'
            event_check = np.array(event_check)
            event = w.eval(t)
            self.assertTrue(np.isclose(event, event_check).all())

    def test_Worldline_proper_time(self):
        w0 = st.Worldline([[0, 0], [1, 0.9], [2, 0]])
        tau0 = (2 ** 2 - 1.8 ** 2) ** 0.5

        test_cases = [
            # worldline, time0, time1, tau_check
            (w0, 0, 2, tau0),
            (w0, 0, 1, tau0 / 2),
            (w0, 1, 2, tau0 / 2),
            (w0, 0.5, 1.5, tau0 / 2),
            (w0, 0.25, 0.75, tau0 / 4),
            (w0, 1.25, 1.75, tau0 / 4),
            (w0, 0, 0, 0),
            (w0, 0, 0.123, 0.123 * tau0 / 2),
            (w0, 0.123, 0.123, 0),
            (w0, 1, 1, 0),
            (w0, 1.234, 1.234, 0),
            (w0, 2, 2, 0),
        ]

        for w, time0, time1, tau_check in test_cases:
            self.assertAlmostEqual(w.proper_time(time0, time1), tau_check)
            self.assertAlmostEqual(w.proper_time(time1, time0), tau_check)

if __name__ == '__main__':
    unittest.main()
