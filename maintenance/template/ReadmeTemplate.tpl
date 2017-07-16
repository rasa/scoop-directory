# awesome-scoop
A collection of awesome resource for the scoop package manager for windows

# Third party buckets by popularity
{% for repo in sortedrepos %}
[{{cache[repo]['url']}}]({{cache[repo]['url']}})
{% for entry in cache[repo]['entries'] -%}
{{"  * [" + entry + "]("+ cache[repo]['url'] + "/blob/master/" + entry + ".json)"}}
{% endfor -%}
{{'\n'}}
{% endfor -%}