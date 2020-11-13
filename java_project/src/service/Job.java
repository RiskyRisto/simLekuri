package service;

import java.io.IOException;

import org.javasim.RestartException;
import org.javasim.Scheduler;
import org.javasim.SimulationException;
import org.javasim.SimulationProcess;

public class Job extends SimulationProcess {

	public void run() {
		full = false;
		ResponseTime = 0.0;
		ArrivalTime = Scheduler.currentTime();
		
		full = (MachineShop.Q.QueueSize() >= 3);
		try {
			if (!full) {
				MachineShop.TotalJobs++;
				if (!MachineShop.Q.Reserve(this))
					passivate();
				hold(MachineShop.ServiceTime.getNumber());
				car2 = (Job) MachineShop.Q.Liberate();
				if (!(car2 == null))
					car2.activate();
				ResponseTime = Scheduler.currentTime() - ArrivalTime;
				MachineShop.TotalResponseTime += ResponseTime;
				MachineShop.ProcessedJobs++;
			} else {
				MachineShop.LostJobs++;
			}
			terminate();
		} catch (SimulationException e) {
		} catch (RestartException e) {
		} catch (IOException e) {
		}
	}

	public void finished() {
	}

	private double ResponseTime;
	private double ArrivalTime;
	private boolean full;
	public Job car2;

};