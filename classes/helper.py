### Helper Class
### Contains static methods that can be used in various classes. Provides auxiliary helper functions.

import requests
import wikipedia

class Helper:
    @staticmethod
    # Static method to call Wikipedia API, parse response, and return definition (if found).
    def wikipediaAPI(query: str) -> str:
        def defaultQuery(q):
            if not q:
                return None

            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{q}"

            try:
                response = requests.get(url, verify = None)
                response.raise_for_status()
            except requests.RequestException:
                return None
            
            data = response.json()
                
            if data.get("type") == "standard": # normal page case
                extract = data.get("extract")
                return str(extract) if extract else None
            
            elif data.get("type") == "disambiguation":
                try:
                    return str(wikipedia.summary(q)) # will always raise error
                except wikipedia.DisambiguationError as e:
                    firstOption = e.options[0] if e.options else None # takes first page out of disambiguation pages
                    if firstOption:
                        try:
                            return str(wikipedia.summary(firstOption))   
                        except Exception:
                            return None
                    return None
                except Exception:
                    return None
            return None
        
        def specialQuery(q):
            # case two
            # for each word in query, capitalize the first letter e.g. "hello world" -> "Hello_World"
            q = "_".join(word.capitalize() for word in q.split("_"))
            return defaultQuery(q)

        # return actual query or error
        query = query.strip().replace(" ", "_").capitalize() # removes trailing spaces, and replaces spaces with underscores and capitalizes the first letter
        result = defaultQuery(query)
        if result:
            return result
        else:
            return specialQuery(query)

    @staticmethod
    # Performs quicksort on entry objects based on various attributes: alphabeticalAscending, alphabeticalDescending, dateAscending, dateDescending
    # NOTE: Modified pseudocode naming to be more general.
    def quickSort(entries,attribute):
        if len(entries) <= 1:
            return entries
        pivot = entries[0]
        lesser = []
        greater = []

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
                if entry.createdAt < pivot.createdAt:
                    lesser.append(entry)
                else:
                    greater.append(entry)

            elif attribute == "dateDescending":
                if entry.createdAt > pivot.createdAt:
                    lesser.append(entry)
                else:
                    greater.append(entry)
        
        sortedLesser = Helper.quickSort(lesser,attribute)
        sortedGreater = Helper.quickSort(greater,attribute)
        return sortedLesser + [pivot] + sortedGreater

