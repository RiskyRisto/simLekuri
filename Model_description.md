# Process based approach

## Arrivals: generate new patients
## Patient
- Time when patient enters system tStart
- Time when patient exits system tEnd
- Time when patient starts to wait to get to recovery tStartedWaiting
- Time when patient stops waiting to get to recovery tEndWaiting
## Preparation service (queue)
## Operation service (queue with one slot)
## Recovery service (queue)
## Reporter (statistics)
- decide which components will be active processes (with own life cycles)
## Patient
- sketch the life-cycles (ordered (conditional) sequence of actions that change the system variables or manipulate other life-cycles
- arrivals
- create new patient 
- tStart = now()
- schedule arrival for new patient
- Operation service
- tStartedWaiting = now() + surgeryTime
- Recovery service
- tEndWaiting = now()
- tEnd = now() + timeInRecovery
#Additional feature
- During the preparation, some new information is found and the surgery needs to be cancelled
cancelling probability needed
skip the operation and recovery phases
