# Generated by Django 3.2.19 on 2023-07-07 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '9670_improve_bulk_load_performance'),
    ]

    forward_sql = """
        CREATE OR REPLACE FUNCTION public.__arches_create_resource_x_resource_relationships(IN tile_id uuid)
        RETURNS boolean
        LANGUAGE 'plpgsql'
        VOLATILE
        PARALLEL UNSAFE
        COST 100
    
        AS $BODY$
        DECLARE
            resourceinstancefrom_id uuid;
            from_graphid uuid;
            relational_count text;
            val boolean = true;
        BEGIN
            select count(*) into relational_count from tiles where tiledata::text like '%resourceX%' and tileid = tile_id;

            IF relational_count = '0' 
                THEN 
                RETURN false;
            END IF; 
                
            --https://dbfiddle.uk/?rdbms=postgres_12&fiddle=21e25754f355a492dfd7b4a134182d2e

            SELECT resourceinstanceid INTO resourceinstancefrom_id FROM tiles WHERE tileid = tile_id; 
            SELECT graphid INTO from_graphid FROM resource_instances WHERE resourceinstanceid = resourceinstancefrom_id; 

            DELETE FROM resource_x_resource WHERE tileid = tile_id;

            WITH updated_tiles as (
                select * from tiles t
                WHERE
                    t.tileid = tile_id
            )
            , relationships AS (
                SELECT n.nodeid, n.config,
                    jsonb_array_elements(tt.tiledata->n.nodeid::text) AS relationship
                FROM updated_tiles tt
                    LEFT JOIN nodes n ON tt.nodegroupid = n.nodegroupid
                WHERE n.datatype IN ('resource-instance-list', 'resource-instance')
                    AND tt.tiledata->>n.nodeid::text IS NOT null
            )
            , relationships2 AS (
                SELECT r.nodeid, r.config, r.relationship, (SELECT ri.graphid
                    FROM resource_instances ri
                    WHERE (r.relationship->>'resourceId')::uuid = ri.resourceinstanceid) AS to_graphid
                FROM relationships r
            )
            , relationships3 AS (
                SELECT fr.nodeid, fr.relationship, fr.to_graphid, 
                (
                    SELECT graphs->>'ontologyProperty'
                    FROM jsonb_array_elements(fr.config->'graphs') AS graphs
                    WHERE graphs->>'graphid' = fr.to_graphid::text
                ) AS defaultOntologyProperty,
                (
                    SELECT graphs->>'inverseOntologyProperty'
                    FROM jsonb_array_elements(fr.config->'graphs') AS graphs
                    WHERE graphs->>'graphid' = fr.to_graphid::text
                ) AS defaultInverseOntologyProperty
                FROM relationships2 fr
            )

            INSERT INTO resource_x_resource (
                resourcexid,
                notes,
                relationshiptype,
                inverserelationshiptype,
                resourceinstanceidfrom,
                resourceinstanceidto,
                resourceinstancefrom_graphid,
                resourceinstanceto_graphid,
                tileid,
                nodeid,
                created,
                modified
            ) (SELECT
                CASE relationship->>'resourceXresourceId'
                    WHEN '' THEN uuid_generate_v4()
                    ELSE (relationship->>'resourceXresourceId')::uuid
                END,
                '',
                CASE relationship->>'ontologyProperty'
                    WHEN '' THEN defaultOntologyProperty
                    ELSE relationship->>'ontologyProperty'
                END,
                CASE relationship->>'inverseOntologyProperty'
                    WHEN '' THEN defaultInverseOntologyProperty
                    ELSE relationship->>'inverseOntologyProperty'
                END,
                resourceinstancefrom_id,
                (relationship->>'resourceId')::uuid,
                from_graphid,
                to_graphid,
                tile_id,
                nodeid,
                now(),
                now()
            FROM relationships3);
            RETURN val;
        END;
        $BODY$;
    """

    reverse_sql = """
        CREATE OR REPLACE FUNCTION public.__arches_create_resource_x_resource_relationships(IN tile_id uuid)
        RETURNS boolean
        LANGUAGE 'plpgsql'
        VOLATILE
        PARALLEL UNSAFE
        COST 100
    
        AS $BODY$
        DECLARE
            resourceinstancefrom_id uuid;
            from_graphid uuid;
            relational_count text;
            val boolean = true;
        BEGIN
            select count(*) into relational_count from tiles where tiledata::text like '%resourceX%' and tileid = tile_id;

            IF relational_count = '0' 
                THEN 
                RETURN false;
            END IF; 
                
            --https://dbfiddle.uk/?rdbms=postgres_12&fiddle=21e25754f355a492dfd7b4a134182d2e

            SELECT resourceinstanceid INTO resourceinstancefrom_id FROM tiles WHERE tileid = tile_id; 
            SELECT graphid INTO from_graphid FROM resource_instances WHERE resourceinstanceid = resourceinstancefrom_id; 

            DELETE FROM resource_x_resource WHERE tileid = tile_id;

            WITH updated_tiles as (
                select * from tiles t
                WHERE
                    t.tileid = tile_id
            )
            , relationships AS (
                SELECT n.nodeid, n.config,
                    jsonb_array_elements(tt.tiledata->n.nodeid::text) AS relationship
                FROM updated_tiles tt
                    LEFT JOIN nodes n ON tt.nodegroupid = n.nodegroupid
                WHERE n.datatype IN ('resource-instance-list', 'resource-instance')
                    AND tt.tiledata->>n.nodeid::text IS NOT null
            )
            , relationships2 AS (
                SELECT r.nodeid, r.config, r.relationship, (SELECT ri.graphid
                    FROM resource_instances ri
                    WHERE r.relationship->>'resourceId' = ri.resourceinstanceid::text) AS to_graphid
                FROM relationships r
            )
            , relationships3 AS (
                SELECT fr.nodeid, fr.relationship, fr.to_graphid, 
                (
                    SELECT graphs->>'ontologyProperty'
                    FROM jsonb_array_elements(fr.config->'graphs') AS graphs
                    WHERE graphs->>'graphid' = fr.to_graphid::text
                ) AS defaultOntologyProperty,
                (
                    SELECT graphs->>'inverseOntologyProperty'
                    FROM jsonb_array_elements(fr.config->'graphs') AS graphs
                    WHERE graphs->>'graphid' = fr.to_graphid::text
                ) AS defaultInverseOntologyProperty
                FROM relationships2 fr
            )

            INSERT INTO resource_x_resource (
                resourcexid,
                notes,
                relationshiptype,
                inverserelationshiptype,
                resourceinstanceidfrom,
                resourceinstanceidto,
                resourceinstancefrom_graphid,
                resourceinstanceto_graphid,
                tileid,
                nodeid,
                created,
                modified
            ) (SELECT
                CASE relationship->>'resourceXresourceId'
                    WHEN '' THEN uuid_generate_v4()
                    ELSE (relationship->>'resourceXresourceId')::uuid
                END,
                '',
                CASE relationship->>'ontologyProperty'
                    WHEN '' THEN defaultOntologyProperty
                    ELSE relationship->>'ontologyProperty'
                END,
                CASE relationship->>'inverseOntologyProperty'
                    WHEN '' THEN defaultInverseOntologyProperty
                    ELSE relationship->>'inverseOntologyProperty'
                END,
                resourceinstancefrom_id,
                (relationship->>'resourceId')::uuid,
                from_graphid,
                to_graphid,
                tile_id,
                nodeid,
                now(),
                now()
            FROM relationships3);
            RETURN val;
        END;
        $BODY$;
    """

    operations = [
        migrations.RunSQL(forward_sql, reverse_sql),
    ]
