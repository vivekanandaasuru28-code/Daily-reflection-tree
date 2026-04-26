from flask import Flask, render_template, request

app = Flask(__name__)

class ReflectionAgent:

    def __init__(self, completed, quality, time_util, distraction, clarity):
        self.completed = completed
        self.quality = quality
        self.time_util = time_util
        self.distraction = distraction
        self.clarity = clarity

    def evaluate(self):

        trace = []

        # Step 1: Commitment Check
        if self.completed == "yes":
            trace.append("Step 1: Commitments completed → YES")
            
            # Step 2: Quality Check
            if self.quality == "high":
                trace.append("Step 2: Output quality HIGH → Effective Day")
                return {
                    "result": "✅ EFFECTIVE DAY",
                    "trace": trace
                }
            else:
                trace.append("Step 2: Output quality LOW → Move to Gap Analysis")

        else:
            trace.append("Step 1: Commitments completed → NO → Move to Gap Analysis")

        # Step 3: Gap Identification
        if self.clarity == "unclear":
            gap = "Clarity Gap"
            trace.append("Step 3: Clarity UNCLEAR → Clarity Gap")

        elif self.time_util < 5:
            gap = "Execution Gap"
            trace.append(f"Step 3: Time Utilization = {self.time_util} < 5 → Execution Gap")

        elif self.distraction == "high":
            gap = "Discipline Gap"
            trace.append("Step 3: Distraction HIGH → Discipline Gap")

        else:
            gap = "Skill Gap"
            trace.append("Step 3: Default → Skill Gap")

        # Step 4: Root Cause + Action
        if gap == "Clarity Gap":
            action = "Break task into smaller steps before starting"
        elif gap == "Execution Gap":
            action = "Use time-blocking and prioritize tasks"
        elif gap == "Discipline Gap":
            action = "Remove distractions (phone/social media)"
        else:
            action = "Allocate time to learn missing skill"

        trace.append(f"Step 4: Gap = {gap}")
        trace.append(f"Step 5: Action = {action}")

        return {
            "result": f"⚠️ {gap}",
            "action": action,
            "trace": trace
        }


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    action = None
    trace = []

    if request.method == "POST":
        completed = request.form["completed"]
        quality = request.form["quality"]
        time_util = int(request.form["time_util"])
        distraction = request.form["distraction"]
        clarity = request.form["clarity"]

        agent = ReflectionAgent(completed, quality, time_util, distraction, clarity)
        output = agent.evaluate()

        result = output.get("result")
        action = output.get("action")
        trace = output.get("trace")

    return render_template("index.html", result=result, action=action, trace=trace)


if __name__ == "__main__":
    app.run(debug=True)