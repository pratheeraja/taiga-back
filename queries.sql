-- Función para aplanar un array de arrays sólo al primer nivel

CREATE OR REPLACE FUNCTION public.reduce_dim(anyarray)
RETURNS SETOF anyarray AS
$function$
DECLARE
    s $1%TYPE;
BEGIN
    FOREACH s SLICE 1  IN ARRAY $1 LOOP
        RETURN NEXT s;
    END LOOP;
    RETURN;
END;
$function$
LANGUAGE plpgsql IMMUTABLE;

-- Creando tags para us, task e issues

WITH
    object_tags AS (
	SELECT project_id, unnest(tags) AS text FROM userstories_userstory
	UNION
	SELECT project_id, unnest(tags) AS text FROM tasks_task
	UNION
	SELECT project_id, unnest(tags) AS text FROM issues_issue),
    tag_colors AS (
        SELECT id project_id, reduce_dim(tags_colors) tags_colors
        FROM projects_project
        WHERE tags_colors  != '{}'
    )

INSERT INTO tags_tag(project_id, text, color)
SELECT object_tags.project_id, object_tags.text, tags_colors[2]
FROM object_tags
LEFT JOIN tag_colors ON
    tag_colors.project_id = object_tags.project_id AND
    tag_colors.tags_colors[1] =  object_tags.text;

-- Creando tagged items para us, tasks e issues
-- TODO: cuidado con los ID's de los contenty_types
WITH
    object_tags AS (
	SELECT id object_id, project_id, unnest(tags) AS text, 21 content_type_id FROM userstories_userstory
	UNION
	SELECT id object_id, project_id, unnest(tags) AS text, 22 content_type_id FROM tasks_task
	UNION
	SELECT id object_id, project_id, unnest(tags) AS text, 23 content_type_id FROM issues_issue)

INSERT INTO tags_tagged_item (tag_id, object_id, content_type_id)
SELECT tags_tag.id, object_tags.object_id, object_tags.content_type_id
FROM object_tags
JOIN tags_tag ON
    tags_tag.project_id = object_tags.project_id AND
    tags_tag.text =  object_tags.text;

-- Creando todo lo relacionado con proyectos
-- TODO: cuidado con los ID's de los contenty_types
WITH
    object_tags AS (
	SELECT id project_id, unnest(tags) AS text, 10 content_type_id FROM projects_project
    ),
    tag_colors AS (
        SELECT id project_id, reduce_dim(tags_colors) tags_colors
        FROM projects_project
        WHERE tags_colors  != '{}'
    ),
    -- Guardamos los resultados de la inserción de los tags de proyecto
    inserted_tags_tag AS (
	INSERT INTO tags_tag(project_id, text, color)
	SELECT object_tags.project_id, object_tags.text, tags_colors[2]
	FROM object_tags
	LEFT JOIN tag_colors ON
	    tag_colors.project_id = object_tags.project_id AND
	    tag_colors.tags_colors[1] =  object_tags.text
	RETURNING *
    )
    -- Esos resultados de la inserción los usamos para crear los tagged items
    INSERT INTO tags_tagged_item (tag_id, object_id, content_type_id)
    SELECT inserted_tags_tag.id, object_tags.project_id, object_tags.content_type_id
    FROM object_tags
    JOIN inserted_tags_tag ON
	inserted_tags_tag.project_id = object_tags.project_id AND
	inserted_tags_tag.text =  object_tags.text;

-- En los tags de proyecto setamos project_id a nulo
UPDATE tags_tag
SET project_id = null
FROM tags_tagged_item
WHERE
    tags_tag.id = tags_tagged_item.tag_id AND
    tags_tagged_item.content_type_id = 10;
