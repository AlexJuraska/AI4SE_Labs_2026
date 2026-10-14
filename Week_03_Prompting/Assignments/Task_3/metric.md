## Tokens per Correct Answer (TPCA)

This proposed metric shows how many tokens each framework needed to generate one correct answer. The calculation of it is as follows

$ \text{TPCA} = \frac{\text{total output tokens}}{\text{number of correct answers}} $

This works by combining the quality of the result with the needed output cost into one number. It can be used to rank two solutions with similar accuracy, since one may be creating a shorter, therefore also a cheaper, solution, to get essentially the same results. We used only output tokens because they are the part of the cost that the prompting framework directly controls, since the framework shapes how long and detailed the model's response is.

Applying this to our data we get


| Method | Correct Answers | Tokens | TPCA |
| :---: | :---: | :---: | :---: |
| APE | 115 | 14K | 121.74 |
| RFT | 140 | 11K | 78.57 |
| STAR | 155 | 15K | 96.77 |

From this we can see that in this metric, RFT was the most effective with its tokens compared to the achieved accuracy.

TPCA does not replace accuracy or time, but complements them. Accuracy only measures whether the answers are correct, and it can no longer distinguish between methods once it reaches a 100%. Time measures cost, but it is also affected by external factors such as server load and network latency, so the same prompt can take a different amount of time on different runs. TPCA measures how much work the model needed for each correct answer, without being affected by outside conditions. Together, the three metrics show how good the answers are (accuracy), how long they took (time), and how costly they were (TPCA).