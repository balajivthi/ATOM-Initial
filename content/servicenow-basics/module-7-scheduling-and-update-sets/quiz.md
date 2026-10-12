# Quiz: Scheduling & Update Sets

Answer these questions about scheduled imports and update sets. Your score is saved, and reasoning is revealed after you submit.

1. What makes a data source run automatically on a timer?
   A. A business rule
   B. A scheduled import (scheduled data source)
   C. An ACL
   D. A form design
   CORRECT: B
   EXPLAIN: A Scheduled Import record wraps a data source and runs it once or on a repeating schedule, loading and transforming new data automatically.

2. To feed NEW data to a scheduled import, you typically:
   A. Create a new table
   B. Replace the attachment on the data source with the new file
   C. Delete the old transform map
   D. Change the target table
   CORRECT: B
   EXPLAIN: The scheduled job loads whatever file is attached to the data source, so swapping the attachment feeds it fresh data.

3. What are update sets used for?
   A. Scheduling imports
   B. Packaging and moving configuration between instances
   C. Creating users
   D. Sending emails
   CORRECT: B
   EXPLAIN: Update sets collect your configuration changes into a portable unit that can be exported as XML and imported (previewed/committed) on another instance.

4. Which update set state enables the "Export XML" option?
   A. Draft
   B. In Progress
   C. Complete
   D. Deleted
   CORRECT: C
   EXPLAIN: Marking an update set Complete closes it to new changes and enables the Export XML related link.

5. After importing an update set on a target instance, what should you do BEFORE applying it?
   A. Nothing — it applies automatically
   B. Preview Update Set
   C. Delete the XML file
   D. Restart the instance
   CORRECT: B
   EXPLAIN: Preview checks whether the target instance is ready (plugins, conflicts) without applying anything; then you Commit Update Set.
