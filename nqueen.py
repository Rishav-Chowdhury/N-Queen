from __future__ import division
from itertools import permutations, combinations
import copy as cp
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

#Sidebar_Section
st.set_page_config(page_title='N-Queen', layout='centered', initial_sidebar_state='expanded')
st.sidebar.markdown("# N-Queen Problem")
st.sidebar.markdown("### _Rishav Chowdhury_")
st.sidebar.markdown("#####    ")
st.sidebar.markdown("#### The N Queen is the problem of placing N chess queens on an N×N chessboard so that no two queens attack each other by being in the same row, column, diagonal. The expected output is a binary matrix which has 1s for the blocks where the queens are placed.")
st. sidebar.markdown("#####    ")
st.sidebar.markdown("#### This Web Application takes the number of queens as an input on the slider and computes the solutions by *Backtracking* and uses *PyPlot* to display the unique solutions visually.")
st.sidebar.markdown("# ")
st.sidebar.markdown("# ")
st.sidebar.markdown("# ")
st.sidebar.markdown("## About the Author:")
st.sidebar.markdown("#### I am a Full Stack Developer, proficient in several frameworks like React, Node, Angular and Vue. I specialize in designing Websites and Web Applications with interactive UI. I am also a ML novice and have programmed a handful of models for various Med-Tech Hackathons. ")
link1 = '[My Portfolio](https://rishav-chowdhury.github.io/)'
link2 = '[My GitHub](https://github.com/Rishav-Chowdhury)'
link3 = '[My Instagram](https://www.instagram.com/antisocial._.extrovert/)'
st.sidebar.markdown("# ")
st.sidebar.markdown(link1, unsafe_allow_html=True)
st.sidebar.markdown(link2, unsafe_allow_html=True)
st.sidebar.markdown(link3, unsafe_allow_html=True)

#Introducion
st.title("N-Queen Problem")
st.markdown("# ")
st.markdown("## Introduction")
st.markdown("### The eight queens puzzle is the problem of placing eight chess queens on an 8×8 chessboard so that no two queens threaten each other; thus, a solution requires that no two queens share the same row, column, or diagonal. The eight queens puzzle is an example of the more general n queens problem of placing n non-attacking queens on an n×n chessboard, for which solutions exist for all natural numbers n with the exception of n = 2 and n = 3. The only trivial solution exists for n=1.")
st.markdown("# ")

#Possible Solutions
st.markdown("## Input")
st.markdown("### Enter _*n*_ which is the dimension of your Chess Board.")
st.markdown("# ")
N = st.slider('How big is your chess board?', min_value=1, max_value=8)
x = range(1, N + 1)
master_list = []
for item in permutations(range(1, N + 1)):
    y = item
    new_list = []
    for x_value, y_value in zip(x, y):
        new_list.append((x_value, y_value))
    master_list.append(new_list)


def IsDiagonal(point1, point2):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    gradient = (y2 - y1) / (x2 - x1)
    if gradient == -1 or gradient == 1:
        return(True)
    else:
        return(False)


solutions = []
for possible_solution in master_list:
    diagonal_clash_list = []
    for piece1, piece2 in combinations(possible_solution, 2):
        diagonal_clash_list.append(IsDiagonal(piece1, piece2))

    if True not in diagonal_clash_list:
        solutions.append(possible_solution)

solutions = [set(solution) for solution in solutions]

st.markdown("# ")
st.markdown("## Possible Solutions")
with st.beta_expander("Show Solutions"):
    st.text("Possible Positions of Queens")
    st.dataframe(solutions)

#Unique Solutions

# Define C4 rotation
def c4(points):
    transformed_points = []
    for point in points:
        x, y = point
        transformed_points.append(((N + 1) - y, x))
    return(set(transformed_points))


# Define y=x mirror plane
def mirror(points):
    transformed_points = []
    for point in points:
        x, y = point
        transformed_points.append((y, x))
    return(set(transformed_points))


# Define solutions that are equivalent
def symmetry_equivalent_solutions(solution):
    equivalent_solutions = []
    equivalent_solutions.append(solution)
    equivalent_solutions.append(mirror(solution))
    equivalent_solutions.append(c4(solution))
    equivalent_solutions.append(mirror(c4(solution)))
    equivalent_solutions.append(c4(c4(solution)))
    equivalent_solutions.append(mirror(c4(c4(solution))))
    equivalent_solutions.append(c4(c4(c4(solution))))
    equivalent_solutions.append(mirror(c4(c4(c4(solution)))))
    return(equivalent_solutions)


#remove symmetry equivalent duplicates
unique_solutions = cp.deepcopy(solutions)
for n, solution in enumerate(solutions):
    found_in_solutions = False
    for related_solution in symmetry_equivalent_solutions(solution):
        if related_solution in solutions[n + 1:]:
            found_in_solutions = True
            break
    if found_in_solutions:
        unique_solutions.remove(solution)

st.markdown("# ")
st.markdown("## Unique Solutions")
with st.beta_expander("Show Unique Solutions"):
    st.text("Unique Solutions among Possible Positions:")
    st.dataframe(unique_solutions)

#Display Solutions
# Display solutions

def plot_solution(points, savefile_name=None):
    Z1 = np.zeros(N * N).reshape(N, N)
    for r, x in enumerate(Z1):
        for c, y in enumerate(x):
            if (r + c) % 2 == 0:
                Z1[r, c] = 1
    plt.imshow(Z1, cmap=plt.cm.gray, interpolation='nearest',
               extent=(0.5, N + 0.5, 0.5, N + 0.5))

    row_labels = range(1, N + 1)
    col_labels = [letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"][:N]
    plt.xticks(range(1, N + 1), col_labels)
    plt.yticks(range(1, N + 1), row_labels)
    plt.xlim(0.5, N + 0.5)
    plt.ylim(0.5, N + 0.5)
    ax = plt.gca()
    for line in ax.xaxis.get_ticklines():
        line.set_visible(False)
    for line in ax.yaxis.get_ticklines():
        line.set_visible(False)
    #plt.show()
    for point in points:
        plt.scatter(*point, color='r', s=500)
    if savefile_name:
        plt.savefig(savefile_name)
    #return(plt.gcf())
    
def plot_solutions(list_of_solutions):
    plt.gcf().set_size_inches(20,20)
    for n, solution in enumerate(list_of_solutions):
        plt.subplot(4,4,n+1)
        plot_solution(solution)

fig = plot_solutions(unique_solutions)
st.markdown("# ")
st.markdown("## Visualization of Unique Solutions on a Chessboard")
with st.beta_expander("Show Visualization"): 
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.text("Solutions of N-Queen Problem:")
    st.pyplot(fig)