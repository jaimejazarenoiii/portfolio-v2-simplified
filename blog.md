---
layout: page
title: Blog
subtitle: Thoughts on engineering, tools, and craft
prose: false
---

<div class="blog-categories">
{% assign postsCategory = site.posts | group_by_exp:"post", "post.categories"  %}
{% for category in postsCategory %}
<div class="reveal">
  <h2 class="blog-category__title">
    {% if category.name %}{{ category.name }}{% else %}Uncategorized{% endif %}
  </h2>
  <ul class="blog-list">
    {% for post in category.items %}
    <li class="blog-card">
      <a href="{{ post.url | prepend: site.baseurl }}" class="blog-card__link">
        <span class="blog-card__title">{{ post.title }}</span>
        <span class="blog-card__date">{{ post.date | date: "%d %B %Y" }}</span>
        <span class="blog-card__arrow"><i class="fa-solid fa-arrow-right"></i></span>
      </a>
    </li>
    {% endfor %}
  </ul>
</div>
{% endfor %}
</div>
