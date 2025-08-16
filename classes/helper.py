"""
File: classes/helper.py

Purpose:
    Defines the Helper class, which provides utility static functions for use throughout the Lexes app.
    These static functions provide auxiliary usage including external API calls, and manually coded sorting logic.

Contains:
    - Helper class with static methods for various utilities.
    - Methods:
        - wikipediaAPI: Retrieves a summary from Wikipedia for a given query. Tries to handle disambiguation and errors gracefully and with robustness.
        - quickSort: Sorts a list of entries based on specified attributes.

Naming Conventions:
    - Class names: PascalCase (Helper).
    - Method names: camelCase (wikipediaAPI, quickSort).
    - General code: camelCase.
"""

### Module Imports ###
import requests
import wikipedia

class Helper:
    @staticmethod
    def wikipediaAPI(query: str) -> str | None:
        """
        Static method to call Wikipedia API on query, parse response, and return definition (if found).
        Handles disambiguation and input errors by retrying with modified query formats or returning None (which are caught later and handled as errors).
        Returns string of definition if found or None if not found.

        Data Source: Auto retrieved definition is fetched from WikipediaAPI to provide a comprehensive, accurate, up-to-date definition for a wide range of terms.
        - query (str): The search query for Wikipedia. String as it represents the textually inputted search query.
        """
        def defaultQuery(q):
            if not q: # Existence check
                return None
            if not isinstance(q, str): # Type check
                raise TypeError("Query must be a string")

            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{q}"

            try:
                response = requests.get(url, verify = False)
                response.raise_for_status()
            except requests.RequestException as e:
                print(e)
                return None
            
            data = response.json()
                
            if data.get("type") == "standard": # Normal page case
                extract = data.get("extract")
                return str(extract) if extract else None
            
            elif data.get("type") == "disambiguation": # Disambiguation page case
                try:
                    return str(wikipedia.summary(q))
                except wikipedia.DisambiguationError as e:
                    firstOption = e.options[0] if e.options else None # Takes first page out of disambiguation pages
                    if firstOption:
                        try:
                            return str(wikipedia.summary(firstOption))   
                        except Exception:
                            return None
                    return None
                except Exception:
                    return None
            return None
        
        # Special query format for capitalised words, e.g. "hello world" -> "Hello_World".
        # Only used if defaultQuery fails to find a definition (useful for specific terms like names or titles).
        def specialQuery(q):
            # Capitalises each word in the query and joins with underscores, e.g. "hello world" -> "Hello_World"
            q = "_".join(word.capitalize() for word in q.split("_"))
            return defaultQuery(q)

        # Tries to return a definition from the Wikipedia API of the regular query format.
        query = query.strip().replace(" ", "_") # removes trailing spaces, and replaces spaces with underscores
        result = defaultQuery(query)
        if result: # If result is found, return it
            return result
        else: # If not found, try special query format.
            return specialQuery(query)

    @staticmethod
    def quickSort(entries, attribute) -> list:
        """
        Performs quicksort on Entry objects based on various attributes: alphabeticalAscending, alphabeticalDescending, dateAscending, dateDescending.
        Returns a sorted list of Entry objects.
        - entries (list[Entry]): The list of entry objects to sort. List to allow for iteration.
        - attribute (str): The attribute to sort by. String as it represents the sorting criteria.
        """
        ### Validation ###
        if not isinstance(entries, list):
            raise TypeError("entries must be a list of Entry objects")
        for entry in entries:
            if not hasattr(entry, 'term') or not hasattr(entry, 'createdAt'):
                raise TypeError("entries must be a list of Entry objects with 'term' and 'createdAt' attributes")

        # Base case for recursion: if the list is empty or has one element, it's already sorted.
        if len(entries) <= 1:
            return entries

        pivot = entries[0] # Choose the first element as the pivot
        lesser = [] # List of elements less than the pivot to be sorted recursively
        greater = [] # List of elements greater than the pivot to be sorted recursively

        for entry in entries[1:]:
            if attribute == "alphabeticalAscending":
                if entry.term.lower() < pivot.term.lower():
                    lesser.append(entry)
                else:
                    greater.append(entry)

            elif attribute == "alphabeticalDescending":
                if entry.term.lower() > pivot.term.lower():
                    lesser.append(entry)
                else:
                    greater.append(entry)

            elif attribute == "dateAscending":
                # We can pseudosort by UID instead of date, since UID is created in order and will account for entries with the same createdAt date
                if (entry.createdAt, entry.uid) < (pivot.createdAt, pivot.uid):
                    lesser.append(entry)
                else:
                    greater.append(entry)

            elif attribute == "dateDescending":
                # We can pseudosort by UID instead of date, since UID is created in order and will account for entries with the same createdAt date
                if (entry.createdAt, entry.uid) > (pivot.createdAt, pivot.uid):
                    lesser.append(entry)
                else:
                    greater.append(entry)
        
        # Recursively sort the lesser and greater lists, then combine them with the pivot.
        sortedLesser = Helper.quickSort(lesser, attribute)
        sortedGreater = Helper.quickSort(greater, attribute)
        return sortedLesser + [pivot] + sortedGreater