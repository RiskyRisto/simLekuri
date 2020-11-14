package surgery;

import org.javasim.RestartException;
import org.javasim.Scheduler;
import org.javasim.SimulationEntity;
import org.javasim.SimulationException;

/*
 * simulate surgery
 */
public class Patient extends SimulationEntity {
	private double PreparationserviceTime;
	private double operationServiceTime;
	private double recoveryServiceTime;
	
	private double arrivalTime;
	private double departureTime;
	
	private double tStartedWaiting;
	private double tEndWaiting;
	
	public Patient(double preparationserviceTime, double operationServiceTime, double recoveryServiceTime) {
		PreparationserviceTime = preparationserviceTime;
		this.operationServiceTime = operationServiceTime;
		this.recoveryServiceTime = recoveryServiceTime;
		
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
		this.arrivalTime = Scheduler.currentTime();

		//release locks after getting  to next stage
		try {
			Surgery.preparationQueue.get(this);
			hold(PreparationserviceTime);
			
			Surgery.operationQueue.get(this);
			hold(operationServiceTime);
		
			Surgery.preparationQueue.release();
			
			tStartedWaiting = Scheduler.currentTime();
			Surgery.recoveryQueue.get(this);			
			Surgery.operationQueue.release();
			
			tEndWaiting = Scheduler.currentTime();
			Surgery.nWaited++;
			
			hold(recoveryServiceTime);
			
			Surgery.recoveryQueue.release();

			departureTime = Scheduler.currentTime();
			finished();
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
