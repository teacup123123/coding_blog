---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
---

## Latest blog posts
<div>
{% for post in site.posts %}
	<div>
		<a href="{{ post.url | relative_url }}">
			<h3>{{ post.title }}</h3>
		</a>
		<p> | Posted {{ post.date | date_to_string }} | <b>Tags</b>:
			{% for tag in post.tags %}
				<i>{{tag}}</i> , 
			{% endfor %}
		</p>
	</div>
{% endfor %}
</div>
