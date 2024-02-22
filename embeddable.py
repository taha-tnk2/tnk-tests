# Libraries
import math
import numpy as np
from clientWrapper import ClientWrapper

"""
Creates the basis for objects created to do work with embedded data
"""
class Embeddable():
    
    # Initializes the class.
    def __init__(self, name : str, client : ClientWrapper):
        self.name = name
        self.client = client
        self.get_embedding()

    # The string that will be called to be embedded.
    @property
    def embed_text(self):
        return self.name

    # Embeds the string.
    def get_embedding(self):
        self.embedding = self.client.get_embedding(self.embed_text)
        self.np_embedding = np.asarray(self.embedding)

    # String representation of the class.
    def __repr__(self) -> str:
        return self.__class__.__name__+ "<" + self.name + ">"

"""
Does the work of comparing an embeddable with a list of other embeddables.
"""
class Similarity():

    # The precision with which the rounded list is made.
    ROUNDING_PRECISION = 0.1

    # Initializes the class.
    def __init__(self, embeddable : Embeddable, embeddable_list : list, truncate : int = math.inf):

        self.values = []
        for _embeddable in embeddable_list:
            val = Similarity.get_similarity(_embeddable, embeddable)
            self.values.append([_embeddable, val])

        self.asnp = np.asarray(self.values)
        self.ordered = np.flip(self.asnp[self.asnp[:, 1].argsort()], 0)[:min(len(self.asnp), truncate)]

        self.max = self.ordered[0]
        self.min = self.ordered[len(self.ordered)-1]
        self.range = self.max[1] - self.min[1]
        self.range = 1 if self.range == 0 else self.range

        self.normalized = np.asarray([[val[0], (val[1] - self.min[1]) / self.range] for val in self.ordered])
        self.rounded = np.asarray([[val[0], round(val[1] / self.ROUNDING_PRECISION) * self.ROUNDING_PRECISION] for val in self.normalized])

    # Gets the similarity between two embeddables
    def get_similarity(embed0 : Embeddable, embed1 : Embeddable):
        similarity = np.dot(embed0.np_embedding, embed1.np_embedding)
        return similarity

    # String representation of the class.
    def __repr__(self) -> str:
        return self.rounded
    
def main():
    client = ClientWrapper(True)
    embeddable0 = Embeddable("Test0", client)
    embeddable1 = Embeddable("Test1", client)
    similarity = Similarity.get_similarity(embeddable0, embeddable1)
    print(embeddable0)
    print(embeddable1)
    print("Similarity: " + str(similarity))

if __name__ == "__main__":
    main()