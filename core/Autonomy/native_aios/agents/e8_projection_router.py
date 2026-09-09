import numpy as np

class E8Router:
    def __init__(self):
        self.facets = {
            'midwife': np.array([1,0,0,0,0,0,0,0]),
            'weaver': np.array([0,1,0,0,0,0,0,0]),
            'guardian': np.array([0,0,1,0,0,0,0,0]),
            'quantum': np.array([0,0,0,1,0,0,0,0]),
            'flame': np.array([0,0,0,0,1,0,0,0]),
            'spirit': np.array([0,0,0,0,0,1,0,0]),
            'nox': np.array([0,0,0,0,0,0,1,0]),
            'dot': np.array([0,0,0,0,0,0,0,1]),
            'axiom': np.array([1,1,0,0,0,0,0,0]),
        }
    
    def route(self, input_vec):
        scores = {}
        for name, fvec in self.facets.items():
            sim = np.dot(input_vec, fvec) / (np.linalg.norm(input_vec) * np.linalg.norm(fvec) + 1e-8)
            scores[name] = sim
        best = max(scores, key=scores.get)
        return best, scores

if __name__ == "__main__":
    router = E8Router()
    test = np.random.rand(8)
    print("Routed to:", router.route(test))
