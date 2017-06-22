WITH cleaned_input as (
    SELECT customer_id{% for p in predictors %}
        , CASE WHEN {{ p['name'] }} IS NULL
            THEN {{ p['fill_na'] }}
            ELSE {{ p['name'] }} END
            AS {{ p['name'] }}{% endfor %}{% if train %}
        , income{% endif %}
    FROM customer_attr{% if train %}
    WHERE customer_id % 10 = 0
        AND income IS NOT NULL{% endif %}
)
{% if train %}
SELECT *
FROM cleaned_input
{% else %}
SELECT customer_id
    ,  {{ coefs['intercept'] }}{% for p in predictors %}
        + {{ coefs[p['name']] }}*{{ p['name'] }}{% endfor %}
        AS predicted_income
FROM cleaned_input
{% endif %}