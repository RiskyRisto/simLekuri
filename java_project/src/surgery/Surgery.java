package surgery;

import org.javasim.RestartException;
import org.javasim.Semaphore;
import org.javasim.Simulation;
import org.javasim.SimulationException;
import org.javasim.SimulationProcess;

public class Surgery extends SimulationProcess {

	public static Semaphore preparationQueue;
	public static Semaphore operationQueue;
	public static Semaphore recoveryQueue;
	
	public static int nDeparted;
	public static double tTotal;
	public static int nWaited;
	public static double tRecoveryWaiting;

	public Surgery() {
		preparationQueue = new Semaphore(3);
		operationQueue = new Semaphore();
		recoveryQueue = new Semaphore(3);
	}
	
	public void run() {
		Arrivals arrivals = new Arrivals();
		
		try {
			arrivals.activate();
			
			Simulation.start();
			
			hold(3000);
			
			System.out.println(nDeparted);
			System.out.println("average throughput time: " + (tTotal / nDeparted));
			System.out.println("average blocking time in recovery: " + (tRecoveryWaiting / nWaited));
			
			Simulation.stop();
		
			mainResume();
		} catch (SimulationException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (RestartException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	
	public void await() {
		resumeProcess();
		SimulationProcess.mainSuspend();
	}

}
