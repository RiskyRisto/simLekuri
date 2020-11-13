package service;

import org.javasim.RestartException;
import org.javasim.Simulation;
import org.javasim.SimulationException;
import org.javasim.SimulationProcess;
import org.javasim.stats.PrecisionHistogram;
import org.javasim.streams.RandomStream;
import org.javasim.streams.UniformStream;

public class MachineShop extends SimulationProcess {

	public MachineShop() {
		ServiceTime = new UniformStream(6, 10, 100);
//	ServiceTime = new ExponentialStream(8,100);
	}

	public void run() {
		try {
			PrecisionHistogram Lost = new PrecisionHistogram();
			System.out.println("Arrival rate 8 Service time 6 10");
			Simulation.start();
			Arrivals JobShop = new Arrivals(8);
			mon.activate();

			for (int i = 0; i < 10; i++) {
				JobShop.activate();
				mon.reset(i);
				LostJobs = 0;
				hold(5000);
				Lost.setValue(LostJobs);
				LostJobs = 0;
				JobShop.cancel();
				hold(300);
			}
			mon.report(55);

			System.out.println("Mean Lost " + Lost.mean());
			System.out.println("dev Lost " + Lost.stdDev());

			System.out.println("Total number of jobs present " + TotalJobs);
			System.out.println("Total number of jobs processed " + ProcessedJobs);
			System.out.println("Total response time of " + TotalResponseTime);

			Simulation.stop();

			SimulationProcess.mainResume();
		} catch (SimulationException e) {
		} catch (RestartException e) {
		}

	}

	public void Await() {
		this.resumeProcess();
		SimulationProcess.mainSuspend();
	}

	public static Station Q = new Station();
	public static Reporter mon = new Reporter(100);
	public static double TotalResponseTime = 0.0;
	public static RandomStream ServiceTime;
	public static long TotalJobs = 0;
	public static long ProcessedJobs = 0;
	public static long LostJobs = 0;

};