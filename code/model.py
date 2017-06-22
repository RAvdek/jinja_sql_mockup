import json
from sklearn.linear_model import LinearRegression
from jinja2 import Template
from my_tools import query_to_pandas, query_to_table
import warnings
warnings.filterwarnings("ignore")  # DON'T DO THIS IN REAL LIFE

with open('predictors.json') as f:
    PREDICTORS = json.load(f)
with open('template.sql') as f:
    QUERY_TEMPLATE = f.read()


def get_model_coefs():
    """ Returns a dictionary of coefs from training """
    query = Template(
        QUERY_TEMPLATE
    ).render(
        predictors=PREDICTORS,
        train=True
    )
    print "-- Training query --"
    print query
    data = query_to_pandas(query)
    model = LinearRegression().fit(
        data[[p['name'] for p in PREDICTORS]],
        data['income']
    )
    output = {'intercept': model.intercept_}
    for i, p in enumerate(PREDICTORS):
        output[p['name']] = model.coef_[i]
    return output


def evaluate_model(coefs):
    """ Uses coefs to evaluate a model
    and write output to a table """
    query = Template(
        QUERY_TEMPLATE
    ).render(
        predictors=PREDICTORS,
        train=False,
        coefs=coefs
    )
    print "-- Evaluation query --"
    print query
    query_to_table(query)


if __name__ == "__main__":
    coefs = get_model_coefs()
    evaluate_model(coefs)
