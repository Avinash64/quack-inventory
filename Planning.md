#Planning Notes

Goal : Create an inventory system

Start with discord bot and sqlite



user  

id - generated
discord_id - from bot - not mandatory in case i want to add things later


items

id - generated
name - name
condition - maybe fk
picture - maybe later
category - maybe fk
stored_at - maybe fk
notes/details/stats - maybe category based in a different table

notes: 
    developed on my pc but i want to deploy on my pi so keep that in mind, make database migration easy
