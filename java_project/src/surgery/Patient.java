package surgery;

import org.javasim.RestartException;
import org.javasim.Scheduler;
import org.javasim.SimulationEntity;
import org.javasim.SimulationException;

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
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public void run() {
		this.arrivalTime = Scheduler.currentTime();
	
		try {
			Surgery.preparationQueue.get(this);
			hold(PreparationserviceTime);
			Surgery.preparationQueue.release();
			
			Surgery.operationQueue.get(this);
			hold(operationServiceTime);
			Surgery.operationQueue.release();
			
			tStartedWaiting = Scheduler.currentTime();
			Surgery.recoveryQueue.get(this);			
			tEndWaiting = Scheduler.currentTime();
			Surgery.nWaited++;
			
			hold(recoveryServiceTime);
			Surgery.recoveryQueue.release();

			departureTime = Scheduler.currentTime();
			finished();
			terminate();
			
			
		} catch (RestartException | SimulationException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	
	public void finished() {
		double time = departureTime - arrivalTime;
		double waitingTime = tEndWaiting - tStartedWaiting;
		
		Surgery.nDeparted++;
		Surgery.tRecoveryWaiting += waitingTime;
		Surgery.tTotal += time;
		
	}
	
}
