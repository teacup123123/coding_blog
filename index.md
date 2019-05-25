---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
---

## Latest blog posts:
<div>
{% for post in site.posts %}
  <a href="{{ post.url }}">
    <h3> - {{ post.title }}</h3>
    <p>{{ post.date | date_to_string }}</p>
  </a>
{% endfor %}
</div>
