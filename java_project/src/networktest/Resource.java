package networktest;


import org.javasim.SimulationProcess;

public class Resource {

	/**
	 * Class for critical resource that can be Reserved and Liberated and manages
	 * itself the required waiting list
	 */

	public Resource(int number) {
		Waiting = new ProcessQueue();
		Capacity = number;
		UsedCapacity = 0;
	}

	public Resource() {
		Waiting = new ProcessQueue();
		Capacity = 1;
		UsedCapacity = 0;
	}

	public boolean IsEmpty() {
		if (Waiting.IsEmpty())
			return true;
		else
			return false;
	}

	public long QueueSize() {
		return Waiting.QueueSize();
	}

	public boolean IsBusy() {
		if (UsedCapacity == Capacity)
			return true;
		else
			return false;
	}

	public boolean Reserve(SimulationProcess Client2) {
		if ((Waiting.QueueSize() == 0) && (UsedCapacity < Capacity)) {
			UsedCapacity++;
			if (debug)
				System.out.println("reserve OK, used " + UsedCapacity + " waiting " + Waiting.QueueSize());
			return true;
		} else {
			Waiting.Enqueue(Client2);
			if (debug)
				System.out.println("reserve failed, used " + UsedCapacity + " waiting " + Waiting.QueueSize());
			return false;
		}
	}

	public SimulationProcess Liberate() {
		if (!IsEmpty()) {
			Client = Waiting.Dequeue();
			if (debug)
				System.out.println("liberate for next, used " + UsedCapacity + " waiting " + Waiting.QueueSize());
			return Client;
		} else {
			UsedCapacity--;
			if (debug)
				System.out.println("liberate to empty, used " + UsedCapacity + " waiting " + Waiting.QueueSize());
			return null;
		}
	}

	public void setDebug(boolean set) {
		debug = set;
	}

	public void setBlocked(boolean set) // to be managed by the currently using process for monitoring purposes only
	{
		blocked = set;
	}

	public boolean isBlocked() {
		return blocked;
	}

	public ProcessQueue Waiting;
	public SimulationProcess Client;
	private int Capacity;
	private int UsedCapacity;
	private boolean debug = false;
	private boolean blocked = false;

}