spaCy documentation for vector similarity : https://spacy.io/usage/linguistic-features#vectors-similarity

The similarity of Doc and Span objects defaults to the average of the token vectors. This means that the vector for “fast food” is the average of the vectors for “fast” and “food”, which isn’t necessarily representative of the phrase “fast food”.
Vector averaging means that the vector of multiple tokens is insensitive to the order of the words. Two documents expressing the same meaning with dissimilar wording will return a lower similarity score than two documents that happen to contain the same words while expressing different meanings.

