import csv
import sys

from util import Node, StackFrontier, QueueFrontier
from agent import Searcher

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}



def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    #directory = sys.argv[1] if len(sys.argv) == 2 else "large"
    directory = sys.argv[1] if len(sys.argv) == 2 else "small"
    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")
     
    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    
    




    path = shortest_path(source, target)
"""
    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")
"""

def shortest_path(source, target):
    # The Agent for search the solution
    frontier=StackFrontier()
    SearcherAgent=Searcher(frontier)
    Actual_node=Node({source},None,None)
    SearcherAgent.push_in_frontier([Actual_node])
    neighbors={}
    pre_frontier={}
    #Actual_node=SearcherAgent.pop_frontier()
    
    while not SearcherAgent.is_goal(target, Actual_node) and not SearcherAgent.frontier_is_empty():
        SearcherAgent.add_visited(Actual_node)
        if Actual_node.parent is None:
             Actual_node=SearcherAgent.pop_frontier()
        #Expand de frontier 
        pre_frontier={}
        for id_state in Actual_node.state:
            neighbors= neighbors_for_person(id_state)
            pre_frontier[id_state]={}
            #prepare list of movies
            movies_list=set()
            for par in neighbors:
                if par[0] not in movies_list:
                   movies_list.add(par[0])
             #prepare  pre_frontier     
            for movie in movies_list:
                pre_frontier[id_state][movie]=set()
                for par in neighbors:
                    if movie in par:
                        if not SearcherAgent.is_visited(par[1]):
                            pre_frontier[id_state][movie].add(par[1])
        #Create list to add to frontier
        list_frontier=[]
        for father in pre_frontier:
            for action in pre_frontier[father]:
                new_node=Node(pre_frontier[father][action],father,action)
                list_frontier.append(new_node)
            # add to frontier
        SearcherAgent.push_in_frontier(list_frontier)
        Actual_node=SearcherAgent.pop_frontier()
    
  
    
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # TODO
    #raise NotImplementedError


def person_id_for_name(name):
    
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
