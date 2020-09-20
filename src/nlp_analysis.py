"""This module contains functions to do NLP analysis of the Gaysian Diaries and Gaysian
Third Space blog posts."""

import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

def word_count(text):
    """Return the word count of the text as an int."""
    return len(text.split())


def median_sentiment_score(text):
    """Calculates the VADER compound sentiment score for each sentence in the text and
    returns the median compound sentiment score."""
    # Only return a calculated median score if there is text; otherwise, return 0 as default score
    if text:
        compound_scores = np.array([analyzer.polarity_scores(sent)['compound'] for sent in text])
        return np.median(compound_scores)
    return 0


def mean_sentiment_score(text):
    """Calculates the VADER compound sentiment score for each sentence in the text
    and returns the mean compound sentiment score."""
    # Only return a calculated mean score if there is text; otherwise, return 0 as default score
    if text:
        compound_scores = np.array([analyzer.polarity_scores(sent)['compound'] for sent in text])
        return np.mean(compound_scores)
    return 0


def beginning_mean_sentiment_score(text):
    """Calculates the VADER compound sentiment score for each sentence in the first third of the
    text (i.e. the beginning) and returns the mean compound sentiment score."""
    if len(text) >= 3:
        beginning_text = text[:len(text)//3]
        compound_scores = np.array([analyzer.polarity_scores(sent)['compound'] for sent in beginning_text])
        return np.mean(compound_scores)
    return 0


def beginning_median_sentiment_score(text):
    """Calculates the VADER compound sentiment score for each sentence in the first third of the
    text (i.e. the beginning) and returns the median compound sentiment score."""
    if len(text) >= 3:
        beginning_text = text[:len(text)//3]
        compound_scores = np.array([analyzer.polarity_scores(sent)['compound'] for sent in beginning_text])
        return np.median(compound_scores)
    return 0


def middle_mean_sentiment_score(text):
    """Calculates the VADER compound sentiment score for each sentence in the second
    third of the text (i.e. the middle) and returns the mean compound sentiment score."""
    if len(text) >= 3:
        middle_text = text[len(text)//3:len(text)//3*2]
        compound_scores = np.array([analyzer.polarity_scores(sent)['compound'] for sent in middle_text])
        return np.mean(compound_scores)
    return 0


def middle_median_sentiment_score(text):
    """Calculates the VADER compound sentiment score for each sentence in the second
    third of the text (i.e. the middle) and returns the median compound sentiment score."""
    if len(text) >= 3:
        middle_text = text[len(text)//3:len(text)//3*2]
        compound_scores = np.array([analyzer.polarity_scores(sent)['compound'] for sent in middle_text])
        return np.median(compound_scores)
    return 0


def end_mean_sentiment_score(text):
    """Calculates the VADER compound sentiment score for each sentence in the last
    third of the text (i.e. the end) and returns the mean compound sentiment score."""
    if len(text) >= 3:
        end_text = text[len(text)//3*2:]
        compound_scores = np.array([analyzer.polarity_scores(sent)['compound'] for sent in end_text])
        return np.mean(compound_scores)
    return 0


def end_median_sentiment_score(text):
    """Calculates the VADER compound sentiment score for each sentence in the last third of the
    text (i.e. the end) and returns the median compound sentiment score."""
    if len(text) >= 3:
        end_text = text[len(text)//3*2:]
        compound_scores = np.array([analyzer.polarity_scores(sent)['compound'] for sent in end_text])
        return np.median(compound_scores)
    return 0


def most_positive_sentence(text):
    """Returns the most positive sentence in the text based on the highest VADER compound
    sentiment score."""
    if text:
        sent_score_dict = {}
        for sent in text:
            sent_score_dict[sent] = analyzer.polarity_scores(sent)['compound']
        return max(sent_score_dict, key=sent_score_dict.get)
    return None


def most_positive_sentence_score(text):
    """Returns the VADER compound sentiment score for the most positive sentence
    in the text (i.e. the highest compound sentiment score)."""
    if text:
        sent_score_dict = {}
        for sent in text:
            sent_score_dict[sent] = analyzer.polarity_scores(sent)['compound']
        return max(sent_score_dict.values())
    return None


def most_negative_sentence(text):
    """Returns the most negative sentence in the text based on the lowest VADER compound
    sentiment score."""
    if text:
        sent_score_dict = {}
        for sent in text:
            sent_score_dict[sent] = analyzer.polarity_scores(sent)['compound']
        return min(sent_score_dict, key=sent_score_dict.get)
    return None


def most_negative_sentence_score(text):
    """Returns the VADER compound sentiment score for the most negative sentence
    in the text (i.e. the lowest compound sentiment score)."""
    if text:
        sent_score_dict = {}
        for sent in text:
            sent_score_dict[sent] = analyzer.polarity_scores(sent)['compound']
        return min(sent_score_dict.values())
    return None


def section_classifier(text, sentence_index):
    """Returns the name of the section for a sentence in the text.

    Args:
        text: The text as a str.
        sentence_index: Index of the sentence in the text."""
    if (sentence_index) < len(text)//3:
        return 'beginning'
    elif len(text)//3*2 > sentence_index >= len(text)//3:
        return 'middle'
    else:
        return 'end'


def sentiment_classifier(compound_score):
    """Returns the sentiment for a sentence in the text.

    Args:
        compound_score: The VADER compound sentiment score for that sentence."""
    if compound_score >= 0.05:
        return 'positive'
    elif 0.05 > compound_score > -0.05:
        return 'neutral'
    else:
        return 'negative'


def sentence_sentiment_analysis(text):
    """Returns a dict of key information for each sentence in the text."""
    if len(text) >= 3:
        sentence_sentiment_analysis_list = [
            {'sentence': sent,
             'section': section_classifier(text, index),
             'compound_score': analyzer.polarity_scores(sent)['compound'],
             'sentiment': sentiment_classifier(analyzer.polarity_scores(sent)['compound'])}
            for index, sent in enumerate(text)]
        return sentence_sentiment_analysis_list
    return None
