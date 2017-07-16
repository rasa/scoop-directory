# awesome-scoop
A collection of awesome resource for the scoop package manager for windows

# Third party buckets by popularity
{% for key,value in cache.items() -%}
    [{{value['url']}}]
    {% for entry in value['entries'] -%}
        {{"    * "+ "["+ value['url'] + "/blob/master/" + entry + ".json]"}}
    {% endfor -%}
-     
 
{% endfor -%}
