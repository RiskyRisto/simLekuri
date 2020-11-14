package surgery;

import org.javasim.RestartException;
import org.javasim.Semaphore;
import org.javasim.Simulation;
import org.javasim.SimulationException;
import org.javasim.SimulationProcess;

/**
 * Container for the state of the simulation and
 * main part of the simulation starting the processing
 * @author Juha Reinikainen
 *
 */
public class Surgery extends SimulationProcess {

	public static Semaphore preparationQueue;
	public static Semaphore operationQueue;
	public static Semaphore recoveryQueue;
	
	//number of patients who have departed
	public static long nDeparted;
	//total time patients have spent in the system (arrival-departure)
	public static double tTotal;
	
	//number of patients that have waited to get to recovery
	public static long nWaited;
	//total time patients have waited to get to recovery
	public static double tRecoveryWaiting;
	
	//total time operation room has been busy
	public static double tBusy;
	
	//number of patients entered
	public static long nTotal;
	//number of patients in queue (sampled when patient arrives)
	public static long nQeueued;
	
	public static long operationsCancelled;
	
	public Surgery() {
		preparationQueue = new Semaphore(Settings.N_PREPARATION_ROOMS);
		operationQueue = new Semaphore(Settings.N_OPERATION_ROOMS);
		recoveryQueue = new Semaphore(Settings.N_RECOVERY_ROOMS);
	}
	
	
	public void run() {
		Arrivals arrivals = new Arrivals();
		
		try {
			arrivals.activate();
			
			Simulation.start();
			
			hold(Settings.SIMULATION_TIME);			
			
			Simulation.stop();
		
			mainResume();
		} catch (SimulationException e) {
			e.printStackTrace();
		} catch (RestartException e) {
			e.printStackTrace();
		}
		
	}
	
	public void await() {
		resumeProcess();
		SimulationProcess.mainSuspend();
	}

}
