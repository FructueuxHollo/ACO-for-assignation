# ACO-for-assignation
solving static job scheduling problem in the UPC system with ant colony optimization

### ACO vs Randomized Multi-start Local Search.

| #              | 9 jobs            | 18 jobs           | 27 jobs           |
| -------------- | ----------------- | ----------------- | ----------------- |
| Local Search.  | 00:38:29          | 01:09:10          | 01:46:34          |
| Proposal (ACO) | 00:36:09          | 00:36:09          | 00:44:09          |
| Improvement    | 00:02:20 (06.06%) | 00:33:01 (47.73%) | 01:02:25 (58.57%) |

---

### Genetic Algorithm vs Ant Colony Optimization

| Nbr of jobs | Genetic Algorithm | Ant Colony Optimization |       Improvement |
| :---------- | :---------------: | :---------------------: | ----------------: |
| 09          |     00:36:09      |        00:36:09         | 00:00:00 (00.00%) |
| 18          |     00:54:21      |        00:36:09         | 00:18:12 (33.49%) |
| 27          |     01:13:36      |        00:44:09         | 00:29:27 (40.01%) |
| 36          |     01:41:41      |        00:53:47         | 00:47:54 (47.11%) |
| 45          |     02:00:07      |        01:04:41         | 00:55:26 (46.15%) |
| 54          |     02:27:37      |        01:17:54         | 01:09:43 (47.23%) |
| 63          |     02:50:48      |        01:25:53         | 01:24:55 (49.72%) |
| 72          |     03:14:58      |        01:44:24         | 01:30:34 (46.45%) |
| 81          |     03:34:57      |        02:00:12         | 01:34:45 (44.08%) |
| 90          |     04:00:00      |        02:09:07         | 01:50:53 (46.20%) |



Dataset: data/jobs9.csv
Optimal Path: [('Network Simulator', 'PC5'), ('Optimization Algorithm', 'PC2'), ('DCGAN', 'PC3'), ('RNN', 'PC3'), ('CNN', 'PC2'), ('FFmpeg', 'PC4'), ('Converter', 'PC4'), ('Palabos', 'PC2'), ('Flow', 'PC4')]
Total Duration: 0 hours 36 minutes 9 seconds


Dataset: data/jobs18.csv
Optimal Path: [('Network Simulator', 'PC5'), ('Optimization Algorithm', 'PC5'), ('DCGAN', 'PC4'), ('RNN', 'PC2'), ('CNN', 'PC4'), ('FFmpeg', 'PC3'), ('Converter', 'PC5'), ('Palabos', 'PC3'), ('Flow', 'PC5'), ('Network Simulator', 'PC5'), ('Optimization Algorithm', 'PC2'), ('DCGAN', 'PC4'), ('RNN', 'PC2'), ('CNN', 'PC3'), ('FFmpeg', 'PC5'), ('Converter', 'PC3'), ('Palabos', 'PC5'), ('Flow', 'PC5')]
Total Duration: 0 hours 36 minutes 9 seconds


Dataset: data/jobs27.csv
Optimal Path: [('Network Simulator', 'PC4'), ('Optimization Algorithm', 'PC1'), ('DCGAN', 'PC4'), ('RNN', 'PC5'), ('CNN', 'PC3'), ('FFmpeg', 'PC4'), ('Converter', 'PC3'), ('Palabos', 'PC4'), ('Flow', 'PC3'), ('Network Simulator', 'PC4'), ('Optimization Algorithm', 'PC5'), ('DCGAN', 'PC5'), ('RNN', 'PC5'), ('CNN', 'PC4'), ('FFmpeg', 'PC5'), ('Converter', 'PC3'), ('Palabos', 'PC3'), ('Flow', 'PC2'), ('Network Simulator', 'PC5'), ('Optimization Algorithm', 'PC2'), ('DCGAN', 'PC5'), ('RNN', 'PC2'), ('CNN', 'PC3'), ('FFmpeg', 'PC4'), ('Converter', 'PC2'), ('Palabos', 'PC5'), ('Flow', 'PC4')]
Total Duration: 0 hours 44 minutes 9 seconds


Dataset: data/jobs36.csv
Optimal Path: [('Network Simulator', 'PC5'), ('Optimization Algorithm', 'PC4'), ('DCGAN', 'PC5'), ('RNN', 'PC3'), ('CNN', 'PC3'), ('FFmpeg', 'PC4'), ('Converter', 'PC4'), ('Palabos', 'PC5'), ('Flow', 'PC5'), ('Network Simulator', 'PC5'), ('Optimization Algorithm', 'PC5'), ('DCGAN', 'PC4'), ('RNN', 'PC2'), ('CNN', 'PC3'), ('FFmpeg', 'PC4'), ('Converter', 'PC5'), ('Palabos', 'PC3'), ('Flow', 'PC5'), ('Network Simulator', 'PC4'), ('Optimization Algorithm', 'PC4'), ('DCGAN', 'PC5'), ('RNN', 'PC3'), ('CNN', 'PC5'), ('FFmpeg', 'PC5'), ('Converter', 'PC3'), ('Palabos', 'PC5'), ('Flow', 'PC2'), ('Network Simulator', 'PC4'), ('Optimization Algorithm', 'PC2'), ('DCGAN', 'PC3'), ('RNN', 'PC4'), ('CNN', 'PC5'), ('FFmpeg', 'PC5'), ('Converter', 'PC4'), ('Palabos', 'PC5'), ('Flow', 'PC5')]      
Total Duration: 0 hours 53 minutes 47 seconds


Dataset: data/jobs45.csv
Optimal Path: [('Network Simulator', 'PC5'), ('Optimization Algorithm', 'PC3'), ('DCGAN', 'PC3'), ('RNN', 'PC5'), ('CNN', 'PC4'), ('FFmpeg', 'PC4'), ('Converter', 'PC4'), ('Palabos', 'PC2'), ('Flow', 'PC2'), ('Network Simulator', 'PC5'), ('Optimization Algorithm', 'PC4'), ('DCGAN', 'PC5'), ('RNN', 'PC5'), ('CNN', 'PC4'), ('FFmpeg', 'PC4'), ('Converter', 'PC1'), ('Palabos', 'PC4'), ('Flow', 'PC4'), ('Network Simulator', 'PC4'), ('Optimization Algorithm', 'PC5'), ('DCGAN', 'PC3'), ('RNN', 'PC4'), ('CNN', 'PC5'), ('FFmpeg', 'PC3'), ('Converter', 'PC3'), ('Palabos', 'PC3'), ('Flow', 'PC2'), ('Network Simulator', 'PC3'), ('Optimization Algorithm', 'PC1'), ('DCGAN', 'PC4'), ('RNN', 'PC4'), ('CNN', 'PC4'), ('FFmpeg', 'PC2'), ('Converter', 'PC5'), ('Palabos', 'PC4'), ('Flow', 'PC5'), ('Network Simulator', 'PC4'), ('Optimization Algorithm', 'PC5'), ('DCGAN', 'PC5'), ('RNN', 'PC5'), ('CNN', 'PC5'), ('FFmpeg', 'PC5'), ('Converter', 'PC3'), ('Palabos', 'PC2'), ('Flow', 'PC4')]
Total Duration: 1 hours 4 minutes 41 seconds


Dataset: data/jobs54.csv
Optimal Path: [('Network Simulator', 'PC5'), ('Optimization Algorithm', 'PC2'), ('DCGAN', 'PC5'), ('RNN', 'PC3'), ('CNN', 'PC5'), ('FFmpeg', 'PC5'), ('Converter', 'PC4'), ('Palabos', 'PC5'), ('Flow', 'PC5'), ('Network Simulator', 'PC5'), ('Optimization Algorithm', 'PC3'), ('DCGAN', 'PC4'), ('RNN', 'PC5'), ('CNN', 'PC5'), ('FFmpeg', 'PC2'), ('Converter', 'PC4'), ('Palabos', 'PC3'), ('Flow', 'PC5'), ('Network Simulator', 'PC4'), ('Optimization Algorithm', 'PC5'), ('DCGAN', 'PC4'), ('RNN', 'PC5'), ('CNN', 'PC3'), ('FFmpeg', 'PC5'), ('Converter', 'PC1'), ('Palabos', 'PC3'), ('Flow', 'PC5'), ('Network Simulator', 'PC4'), ('Optimization Algorithm', 'PC6'), ('DCGAN', 'PC4'), ('RNN', 'PC4'), ('CNN', 'PC6'), ('FFmpeg', 'PC5'), ('Converter', 'PC5'), ('Palabos', 'PC4'), ('Flow', 'PC4'), ('Network Simulator', 'PC3'), ('Optimization Algorithm', 'PC2'), ('DCGAN', 'PC4'), ('RNN', 'PC3'), ('CNN', 'PC5'), ('FFmpeg', 'PC5'), ('Converter', 'PC3'), ('Palabos', 'PC3'), ('Flow', 'PC4'), ('Network Simulator', 'PC5'), ('Optimization Algorithm', 'PC4'), ('DCGAN', 'PC4'), ('RNN', 'PC6'), ('CNN', 'PC3'), ('FFmpeg', 'PC5'), ('Converter', 'PC2'), ('Palabos', 'PC4'), ('Flow', 'PC4')]
Total Duration: 1 hours 17 minutes 54 seconds


Dataset: data/jobs63.csv
Optimal Path: [('Network Simulator', 'PC4'), ('Optimization Algorithm', 'PC5'), ('DCGAN', 'PC4'), ('RNN', 'PC3'), ('CNN', 'PC5'), ('FFmpeg', 'PC4'), ('Converter', 'PC3'), ('Palabos', 'PC3'), ('Flow', 'PC3'), ('Network Simulator', 'PC5'), ('Optimization Algorithm', 'PC4'), ('DCGAN', 'PC4'), ('RNN', 'PC5'), ('CNN', 'PC4'), ('FFmpeg', 'PC3'), ('Converter', 'PC4'), ('Palabos', 'PC5'), ('Flow', 'PC5'), ('Network Simulator', 'PC4'), ('Optimization Algorithm', 'PC4'), ('DCGAN', 'PC5'), ('RNN', 'PC3'), ('CNN', 'PC5'), ('FFmpeg', 'PC4'), ('Converter', 'PC2'), ('Palabos', 'PC5'), ('Flow', 'PC4'), ('Network Simulator', 'PC2'), ('Optimization Algorithm', 'PC4'), ('DCGAN', 'PC5'), ('RNN', 'PC2'), ('CNN', 'PC3'), ('FFmpeg', 'PC5'), ('Converter', 'PC3'), ('Palabos', 'PC5'), ('Flow', 'PC3'), ('Network Simulator', 'PC4'), ('Optimization Algorithm', 'PC4'), ('DCGAN', 'PC5'), ('RNN', 'PC4'), ('CNN', 'PC3'), ('FFmpeg', 'PC2'), ('Converter', 'PC4'), ('Palabos', 'PC3'), ('Flow', 'PC2'), ('Network Simulator', 'PC3'), ('Optimization Algorithm', 'PC4'), ('DCGAN', 'PC5'), ('RNN', 'PC4'), ('CNN', 'PC5'), ('FFmpeg', 'PC5'), ('Converter', 'PC2'), ('Palabos', 'PC3'), ('Flow', 'PC3'), ('Network Simulator', 'PC5'), ('Optimization Algorithm', 'PC2'), ('DCGAN', 'PC4'), ('RNN', 'PC2'), ('CNN', 'PC3'), ('FFmpeg', 'PC3'), ('Converter', 'PC4'), ('Palabos', 'PC4'), ('Flow', 'PC3')]
Total Duration: 1 hours 25 minutes 53 seconds


Dataset: data/jobs72.csv
Optimal Path: [('Network Simulator', 'PC5'), ('Optimization Algorithm', 'PC5'), ('DCGAN', 'PC5'), ('RNN', 'PC2'), ('CNN', 'PC4'), ('FFmpeg', 'PC4'), ('Converter', 'PC2'), ('Palabos', 'PC5'), ('Flow', 'PC4'), ('Network Simulator', 'PC4'), ('Optimization Algorithm', 'PC5'), ('DCGAN', 'PC4'), ('RNN', 'PC3'), ('CNN', 'PC4'), ('FFmpeg', 'PC5'), ('Converter', 'PC5'), ('Palabos', 'PC5'), ('Flow', 'PC2'), ('Network Simulator', 'PC4'), ('Optimization Algorithm', 'PC6'), ('DCGAN', 'PC4'), ('RNN', 'PC5'), ('CNN', 'PC2'), ('FFmpeg', 'PC5'), ('Converter', 'PC4'), ('Palabos', 'PC6'), ('Flow', 'PC1'), ('Network Simulator', 'PC4'), ('Optimization Algorithm', 'PC3'), ('DCGAN', 'PC4'), ('RNN', 'PC5'), ('CNN', 'PC5'), ('FFmpeg', 'PC5'), ('Converter', 'PC3'), ('Palabos', 'PC5'), ('Flow', 'PC3'), ('Network Simulator', 'PC5'), ('Optimization Algorithm', 'PC4'), ('DCGAN', 'PC4'), ('RNN', 'PC2'), ('CNN', 'PC5'), ('FFmpeg', 'PC4'), ('Converter', 'PC4'), ('Palabos', 'PC4'), ('Flow', 'PC6'), ('Network Simulator', 'PC3'), ('Optimization Algorithm', 'PC5'), ('DCGAN', 'PC5'), ('RNN', 'PC6'), ('CNN', 'PC5'), ('FFmpeg', 'PC3'), ('Converter', 'PC5'), ('Palabos', 'PC2'), ('Flow', 'PC3'), ('Network Simulator', 'PC5'), ('Optimization Algorithm', 'PC4'), ('DCGAN', 'PC4'), ('RNN', 'PC5'), ('CNN', 'PC5'), ('FFmpeg', 'PC3'), ('Converter', 'PC4'), ('Palabos', 'PC2'), ('Flow', 'PC4'), ('Network Simulator', 'PC3'), ('Optimization Algorithm', 'PC3'), ('DCGAN', 'PC3'), ('RNN', 'PC5'), ('CNN', 'PC3'), ('FFmpeg', 'PC5'), ('Converter', 'PC4'), ('Palabos', 'PC3'), ('Flow', 'PC5')]
Total Duration: 1 hours 44 minutes 24 seconds


Dataset: data/jobs81.csv
Optimal Path: [('Network Simulator', 'PC4'), ('Optimization Algorithm', 'PC5'), ('DCGAN', 'PC3'), ('RNN', 'PC5'), ('CNN', 'PC5'), ('FFmpeg', 'PC4'), ('Converter', 'PC4'), ('Palabos', 'PC2'), ('Flow', 'PC6'), ('Network Simulator', 'PC2'), ('Optimization Algorithm', 'PC2'), ('DCGAN', 'PC4'), ('RNN', 'PC5'), ('CNN', 'PC4'), ('FFmpeg', 'PC3'), ('Converter', 'PC4'), ('Palabos', 'PC3'), ('Flow', 'PC5'), ('Network Simulator', 'PC2'), ('Optimization Algorithm', 'PC3'), ('DCGAN', 'PC4'), ('RNN', 'PC5'), ('CNN', 'PC5'), ('FFmpeg', 'PC5'), ('Converter', 'PC5'), ('Palabos', 'PC5'), ('Flow', 'PC2'), ('Network Simulator', 'PC2'), ('Optimization Algorithm', 'PC5'), ('DCGAN', 'PC5'), ('RNN', 'PC5'), ('CNN', 'PC3'), ('FFmpeg', 'PC4'), ('Converter', 'PC3'), ('Palabos', 'PC5'), ('Flow', 'PC5'), ('Network Simulator', 'PC5'), ('Optimization Algorithm', 'PC5'), ('DCGAN', 'PC5'), ('RNN', 'PC3'), ('CNN', 'PC5'), ('FFmpeg', 'PC4'), ('Converter', 'PC5'), ('Palabos', 'PC3'), ('Flow', 'PC3'), ('Network Simulator', 'PC5'), ('Optimization Algorithm', 'PC4'), ('DCGAN', 'PC4'), ('RNN', 'PC5'), ('CNN', 'PC3'), ('FFmpeg', 'PC3'), ('Converter', 'PC2'), ('Palabos', 'PC5'), ('Flow', 'PC5'), ('Network Simulator', 'PC3'), ('Optimization Algorithm', 'PC2'), ('DCGAN', 'PC3'), ('RNN', 'PC4'), ('CNN', 'PC5'), ('FFmpeg', 'PC4'), ('Converter', 'PC5'), ('Palabos', 'PC4'), ('Flow', 'PC5'), ('Network Simulator', 'PC2'), ('Optimization Algorithm', 'PC5'), ('DCGAN', 'PC5'), ('RNN', 'PC2'), ('CNN', 'PC4'), ('FFmpeg', 'PC4'), ('Converter', 'PC3'), ('Palabos', 'PC5'), ('Flow', 'PC3'), ('Network Simulator', 'PC6'), ('Optimization Algorithm', 'PC4'), ('DCGAN', 'PC4'), ('RNN', 'PC1'), ('CNN', 'PC3'), ('FFmpeg', 'PC4'), ('Converter', 'PC5'), ('Palabos', 'PC4'), ('Flow', 'PC3')]
Total Duration: 2 hours 0 minutes 12 seconds


Dataset: data/jobs90.csv
Optimal Path: [('Network Simulator', 'PC3'), ('Optimization Algorithm', 'PC3'), ('DCGAN', 'PC5'), ('RNN', 'PC4'), ('CNN', 'PC2'), ('FFmpeg', 'PC4'), ('Converter', 'PC4'), ('Palabos', 'PC5'), ('Flow', 'PC3'), ('Network Simulator', 'PC5'), ('Optimization Algorithm', 'PC3'), ('DCGAN', 'PC5'), ('RNN', 'PC5'), ('CNN', 'PC3'), ('FFmpeg', 'PC4'), ('Converter', 'PC5'), ('Palabos', 'PC2'), ('Flow', 'PC2'), ('Network Simulator', 'PC2'), ('Optimization Algorithm', 'PC3'), ('DCGAN', 'PC5'), ('RNN', 'PC6'), ('CNN', 'PC5'), ('FFmpeg', 'PC3'), ('Converter', 'PC1'), ('Palabos', 'PC4'), ('Flow', 'PC3'), ('Network Simulator', 'PC5'), ('Optimization Algorithm', 'PC3'), ('DCGAN', 'PC4'), ('RNN', 'PC5'), ('CNN', 'PC5'), ('FFmpeg', 'PC5'), ('Converter', 'PC4'), ('Palabos', 'PC4'), ('Flow', 'PC2'), ('Network Simulator', 'PC5'), ('Optimization Algorithm', 'PC3'), ('DCGAN', 'PC4'), ('RNN', 'PC5'), ('CNN', 'PC4'), ('FFmpeg', 'PC5'), ('Converter', 'PC4'), ('Palabos', 'PC3'), ('Flow', 'PC3'), ('Network Simulator', 'PC2'), ('Optimization Algorithm', 'PC4'), ('DCGAN', 'PC3'), ('RNNwork Simulator', 'PC5'), ('Optimization Algorithm', 'PC3'), ('DCGAN', 'PC4'), ('RNN', 'PC5'), ('CNN', 'PC4'), ('FFmpeg', 'PC5'), ('Converter', 'PC4'), ('Palabos', 'PC3'), ('Flow', 'PC3'), ('Network Simulator', 'PC2'), ('Optimization Algorithm', 'PC4'), ('DCGAN', 'PC3'), ('RNN', 'PC2'), ('CNN', 'PC5'), ('FFmpeg', 'PC5'), ('Converter', 'PC3'), ('Palabos', 'PC4'), ('Flow', 'PC5'), ('Network Simulator', 'PC2'), ('Optimization Algorithm', 'PC5'), ('DCGAN', 'PC5'), ('RNN', 'PC4'), ('CNN', 'PC1'), ('FFmpeg', 'PC3'), ('Converter', 'PC4'), ('Palabos', 'PC3'), ('Flow', 'PC2'), ('Network Simulator', 'PC2'), ('Optimization Algorithm', 'PC3'), ('DCGAN', 'PC4'), ('RNN', 'PC4'), ('CNN', 'PC4'), ('FFmpeg', 'PC5'), ('Converter', 'PC3'), ('Palabos', 'PC4'), ('Flow', 'PC2'), ('Network Simulator', 'PC4'), ('Optimization Algorithm', 'PC5'), ('DCGAN', 'PC4'), ('RNN', 'PC3'), ('CNN', 'PC5'), ('FFmpeg', 'PC4'), ('Converter', 'PC3'), ('Palabos', 'PC3'), ('Flow', 'PC4'), ('Network Simulator', 'PC5'), ('Optimization Algorithm', 'PC2'), ('DCGAN', 'PC3'), ('RNN', 'PC4'), ('CNN', 'PC3'), ('FFmpeg', 'PC3'), ('Converter', 'PC3'), ('Palabos', 'PC2'), ('Flow', 'PC2')]
Total Duration: 2 hours 9 minutes 7 seconds
