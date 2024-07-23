import numpy as np
from collections import defaultdict, OrderedDict

def expand_boolean_polynomial(polynomials, num_vars):
    import itertools

    # Store the results in a dictionary with the x vector as key
    grouped_results = defaultdict(lambda: defaultdict(list))
    vectors = []
    weight_grouped_results = defaultdict(lambda: defaultdict(list))

    def format_term(coeff, k_vector):
        # Convert k_vector into algebraic term using the coefficient
        term = coeff
        vec = []
        for i, k in enumerate(k_vector):
            if k == '1':
                term += f'k{i+1}'
                vec.append(1)
            else:
                vec.append(0)
        return term, vec
    
    def calculate_weight(x_vector):
        # Count the number of '1's in the x_vector
        return x_vector.count('1')

    for poly_vector, poly_coeff in polynomials.items():
        # Split polynomial vector into individual variable indices
        indices = [i for i, bit in enumerate(poly_vector) if bit == '1']

        # Generate all combinations of (x_i + k_i)
        all_combinations = list(itertools.product([0, 1], repeat=len(indices)))

        # Generate output for each combination
        for comb in all_combinations:
            x_vector = ['0'] * num_vars
            k_vector = ['0'] * num_vars
            
            # Create new vectors for x and k based on combination
            for idx, value in zip(indices, comb):
                if value == 1:
                    k_vector[idx] = '1'
                else:
                    x_vector[idx] = '1'
            
            x_key = ''.join(x_vector)
            k_key = ''.join(k_vector)
            term, vec = format_term(poly_coeff, k_vector)
            grouped_results[x_key][k_key].append(poly_coeff)
            vectors.append(vec)
            # Group by weight of x
            weight_grouped_results[calculate_weight(x_key)][x_key].append(term)
    
    # Check for linear independence of coefficient + k vectors
    matrix = np.array(vectors)
    rank = np.linalg.matrix_rank(matrix)
    independent = rank == len(vectors)

    # Print results grouped by weight and x vector
    ordered_weight_groups = OrderedDict(sorted(weight_grouped_results.items()))
    for weight, x_groups in ordered_weight_groups.items():
        print(f"--- Weight {weight} Terms ---")
        for x, terms in x_groups.items():
            combined_terms = " + ".join(terms)
            x_index = ''.join(f'x{i+1}' for i, bit in enumerate(x) if bit == '1')
            print(f"x:{x} is {x_index}({combined_terms})")
    print(f"Total number of resulting monomials: {len(vectors)}")
    print(f"Are all monomials' coefficients with k linearly independent? {'Yes' if independent else 'No'}")


polynomials = {
    '11100': 'a',  
    '00111': 'b',  
    #'10110': '(a+b)',  
    #'01101': '(a+b)',
    '01110': 'a',
    '10101': 'b'
}
num_vars = 5

expand_boolean_polynomial(polynomials, num_vars)
