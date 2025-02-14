{% macro classify_ratings(column_name) %}
    {% set excellent_lower_bound = 4.5 %}
    {% set good_lower_bound = 4.0 %}
    {% set average_lower_bound = 3.0 %}
    CASE
        WHEN {{ column_name }} >= {{ excellent_lower_bound }} THEN 'Excellent'
        WHEN {{ column_name }} >= {{ good_lower_bound }} THEN 'Good'
        WHEN {{ column_name }} >= {{ average_lower_bound }} THEN 'Average'
        ELSE 'Poor'
    END
{% endmacro %}
