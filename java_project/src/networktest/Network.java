package networktest;

import org.javasim.RestartException;
import org.javasim.Simulation;
import org.javasim.SimulationException;
import org.javasim.SimulationProcess;
import org.javasim.streams.ExponentialStream;

public class Network extends SimulationProcess {

	public Network() {
		Q = new Resource[HarbourCount];
		ServiceTime = new ExponentialStream[HarbourCount];
		for (int i = 0; i < HarbourCount; i++) {
			Q[i] = new Resource(1);
		}
	}

	public void run() {
		try {
			inter = new ExponentialStream(40);
			for (int i = 0; i < HarbourCount; i++) {
				ServiceTime[i] = new ExponentialStream(30, i + 1);
			}
			Arrivals A = new Arrivals(inter, ServiceTime, HarbourCount);
			monitor.activate();
			A.activate();
			Simulation.start();
			hold(5000);
			monitor.restart();
			hold(5000);
			monitor.report();
			System.out.println(ProcessedJobs + " " + TotalResponseTime);
			Simulation.stop();

			A.terminate();
			monitor.terminate();
			SimulationProcess.mainResume();
		} catch (SimulationException e) {
		} catch (RestartException e) {
		}
	}

	public void Await() {
		this.resumeProcess();
		SimulationProcess.mainSuspend();
	}

	private static int HarbourCount = 6;
	public static Reporter monitor = new Reporter(10, 6);
	public static ProcessQueue EntQ = new ProcessQueue();
	public static Resource[] Q;
	public static ExponentialStream[] ServiceTime;
	public static ExponentialStream inter;

	public static double TotalResponseTime = 0.0;
	public static long ProcessedJobs = 0;

};