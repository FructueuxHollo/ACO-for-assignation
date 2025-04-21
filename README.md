# ACO-for-assignation
solving static job scheduling problem in the UPC system with ant colony optimization

### ACO vs Randomized Multi-start Local Search.

| #              | 9 jobs         | 18 jobs           | 27 jobs           |
| -------------- | -------------- | ----------------- | ----------------- |
| Local Search.  | 00:38:29       | 01:09:10          | 01:46:34          |
| Proposal (ACO) | 00:36:09       | 00:55:30          | 01:23:15          |
| Improvement    | 00:02:20 (06%) | 00:13:40 (19.76%) | 00:23:19 (21.88%) |

---

### Genetic Algorithm vs Ant Colony Optimization

| Nbr of jobs | Genetic Algorithm | Ant Colony Optimization |
| ----------- | ----------------- | ----------------------- |
| 09          | 00:36:09          | 00:36:09                |
| 18          | 00:54:21          | 00:55:30                |
| 27          | 01:13:36          | 01:23:15                |
| 36          | 01:41:41          | 01:51:00                |
| 45          | 02:00:07          | 02:18:45                |
| 54          | 02:27:37          | 02:46:30                |
| 63          | 02:50:48          | 03:17:34                |
| 72          | 03:14:58          | 03:45:19                |
| 81          | 03:34:57          | 04:14:00                |
| 90          | 04:00:00          | 04:40:49                |
