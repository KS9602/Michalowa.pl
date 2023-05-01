from django import template


register = template.Library()

register.filter(name="liked")


def liked(value, user):
    for i in value:
        if user in i:
            return "xxx"

    return "yyy"

    #                     {% for user in subject.likes.all.value_list%}

    #                         {% if request.user.username in user.nick %}

    # <a href="{% url 'like' subject.id%}"><button class="like_button_liked">LIKE</button></a> {{subject.likes.all.values_list|length}}
    # {% else%}
    # <a href="{% url 'like' subject.id%}"><button class="like_button">LIKE</button></a> {{subject.likes.all.values_list|length}}

    # {% endif %}

    #                     {% endfor %}

    #                 {% endif %}
