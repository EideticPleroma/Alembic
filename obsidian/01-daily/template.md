# {{date:YYYY-MM-DD}}

## Intentions

What do I intend to accomplish today?

- [ ] 

## Progress

What did I work on?

- 

## Blockers

What's blocking progress?

- 

## Insights

What did I learn or realize?

- 

## Tomorrow

What should I focus on next?

- 

---

## Task Review

### Completed Today
```dataview
TASK
FROM "02-project"
WHERE completed
AND completion = date(today)
```

### In Progress
```dataview
TASK
FROM "02-project"
WHERE !completed
AND contains(tags, "in-progress")
```

