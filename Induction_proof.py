from itertools import combinations

def generate_vectors(n, weight):
    """ Generate all binary vectors of length 'n' and given 'weight'. """
    indices = list(range(n))
    vectors = []
    for combo in combinations(indices, weight):
        vector = [0] * n
        for index in combo:
            vector[index] = 1
        vectors.append(tuple(vector))
    return vectors

def is_dominated(v, u):
    """ Check if vector 'v' is dominated by vector 'u'. """
    return all(v[i] <= u[i] for i in range(len(u)))

def has_empty_intersection(w, v):
    """ Check if vectors 'w' and 'v' have empty intersection in support. """
    return all(w[i] + v[i] <= 1 for i in range(len(w)))

def is_correct_weight(v, weight):
    """ Check if vector 'v' has the specified weight. """
    return sum(v) == weight

def build_equations(n, ni, nik, set_U):
    """ Build equations based on given parameters and set U. """
    equations = {}
    alpha_zeros = {}
    
    # Generate all vectors w of length n and weight nik
    ws = generate_vectors(n, nik)
    
    # Generate all vectors v of length n and weight ni
    vs = generate_vectors(n, ni-nik)
    
    for w in ws:
        terms = []
        independent_terms = []
        for u in set_U:
            for v in vs:
                if is_dominated(v, u) and has_empty_intersection(w, v):
                    # XOR v and w to get the polynomial variable
                    v_xor_w = tuple([v[i] ^ w[i] for i in range(n)])
                    if is_correct_weight(v_xor_w, ni):  # Ensure v XOR w has weight ni
                        term = f"alpha_{v} * P_{v_xor_w}(k)"
                        terms.append(term)
                        if v_xor_w in set_U:
                            independent_terms.append(term)
        
        if terms:
            equation = " + ".join(terms) + " = 0"
            equations[w] = equation
            # Check if all terms in equation are independent and from set U
            if sorted(terms) == sorted(independent_terms):
                for term in independent_terms:
                    alpha_var = term.split(" * ")[0]
                    alpha_zeros[alpha_var] = True
    
    return equations, alpha_zeros

# Define parameters
n = 5
ni = 3
nik = 1
set_U = [(1, 1, 1, 0, 0), (0, 0, 1, 1, 1), (0, 1, 1, 1, 0)]

# Build equations and capture zeros
equations, alpha_zeros = build_equations(n, ni, nik, set_U)

# Display the equations
for w, eq in equations.items():
    print(f"T({w}) := {eq}")

# Display which alpha_v can be concluded to be zero
print("\nAlphas that can be concluded to be zero:")
for alpha, _ in alpha_zeros.items():
    print(alpha)
