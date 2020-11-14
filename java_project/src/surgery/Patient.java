package surgery;

import org.javasim.RestartException;
import org.javasim.Scheduler;
import org.javasim.SimulationEntity;
import org.javasim.SimulationException;

/*
 * simulate surgery
 * extends from simulationentity in order to be able to 
 * manipulate semaphores
 */
public class Patient extends SimulationEntity {
	private double PreparationserviceTime;
	private double operationServiceTime;
	private double recoveryServiceTime;
	
	private double arrivalTime;
	private double departureTime;
	
	private double tStartedWaiting;
	private double tEndWaiting;
	
	private boolean cancelOperation;
	
	public Patient(double preparationserviceTime, double operationServiceTime, double recoveryServiceTime, boolean cancelOperation) {
		this.PreparationserviceTime = preparationserviceTime;
		this.operationServiceTime = operationServiceTime;
		this.recoveryServiceTime = recoveryServiceTime;
		this.cancelOperation = cancelOperation;
	}
	

	/*
	 * activates patient
	 */
	public void startPatient() {
		try {
			this.activate();
		} catch (SimulationException | RestartException e) {
			e.printStackTrace();
		}
	}
	
	/*
	 * Simulate patient going through the system
	 * Preparation -> Surgery -> Recovery
	 */
	public void run() {
		//record time patient arrives
		this.arrivalTime = Scheduler.currentTime();

		//add to total the number of patients currently waiting to get to preparation
		Surgery.nQeueued += Surgery.preparationQueue.numberWaiting();
		Surgery.nTotal++;
		
		//release locks after getting  to next stage
		try {
			//queue to preparation facility
			Surgery.preparationQueue.get(this);
			//spend time in preparation
			hold(this.PreparationserviceTime);
			//check for cancellation
			if (this.cancelOperation) {
				Surgery.operationsCancelled++;
				Surgery.preparationQueue.release();
				terminate();
				return;
			}
			//queue to operation
			Surgery.operationQueue.get(this);
			//release one space from preparation
			Surgery.preparationQueue.release();
			//spend time in operation
			hold(operationServiceTime);
			//record time when started waiting to get to recovery
			this.tStartedWaiting = Scheduler.currentTime();
			//queue to recovery
			Surgery.recoveryQueue.get(this);
			//release one space from operation
			Surgery.operationQueue.release();
			//record time when ended waiting to get to recovery
			this.tEndWaiting = Scheduler.currentTime();
			//record number of patients that have waited to get to recovery
			Surgery.nWaited++;
			//spend time in recovery
			hold(recoveryServiceTime);
			//release one space from recovery
			Surgery.recoveryQueue.release();
			//record the time patient deprated
			this.departureTime = Scheduler.currentTime();
			//save stats
			finished();
			//remove the patient from the scheduler queue
			terminate();
			
			
		} catch (RestartException | SimulationException e) {
			e.printStackTrace();
		}
		
	}
	
	
	/*
	 * update statistics in surgery 
	 */
	public void finished() {
		double time = departureTime - arrivalTime;
		double waitingTime = tEndWaiting - tStartedWaiting;
		
		Surgery.nDeparted++;
		Surgery.tRecoveryWaiting += waitingTime;
		Surgery.tTotal += time;
		
		Surgery.tBusy += this.operationServiceTime;
	}
	
}
