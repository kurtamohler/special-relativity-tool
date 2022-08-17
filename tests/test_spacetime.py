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

    def test_Worldline_proper_time(self):
        w = st.Worldline([[0, 0], [1, 0.9], [2, 0]])

        tau_check = (2 ** 2 - 1.8 ** 2) ** 0.5

        self.assertEqual(w.proper_time(0, 1), tau_check / 2)
        self.assertEqual(w.proper_time(0, 1), tau_check / 2)
        self.assertEqual(w.proper_time(0, 1), tau_check / 2)
        self.assertEqual(w.proper_time(0, 2), tau_check)
        self.assertEqual(w.proper_time(1, 2), tau_check / 2)
        self.assertEqual(w.proper_time(0.5, 1.5), tau_check / 2)
        self.assertEqual(w.proper_time(0.5, 1.5), tau_check / 2)

if __name__ == '__main__':
    unittest.main()
