package service;

import java.util.NoSuchElementException;

import org.javasim.SimulationProcess;

public class Station {

	public Station() {
		head = null;
		length = 0;
		busy = false;
	}

	public boolean IsEmpty() {
		if (length == 0)
			return true;
		else
			return false;
	}

	public long QueueSize() {
		return length;
	}

	public boolean IsBusy() {
		return busy;
	}

	public boolean Reserve(Job car2) {
		if (!IsBusy()) {
			busy = true;
			return true;
		} else {
			Enqueue(car2);
			return false;
		}
//	client=customer;
	}

	public SimulationProcess Liberate() {
		if (!IsEmpty()) {
			car = (Job) Dequeue();
			return car;
		} else {
			busy = false;
			return null;
		}
//	return client;

	}

	public SimulationProcess Dequeue() throws NoSuchElementException {
		if (IsEmpty())
			throw (new NoSuchElementException());
		List ptr = head;
		head = head.next;

		length--;

		return ptr.work;
	}

	public void Enqueue(SimulationProcess toadd) {
		if (toadd == null)
			return;
		List ptr = head;

		if (IsEmpty()) {
			head = new List();
			ptr = head;
		} else {
			while (ptr.next != null)
				ptr = ptr.next;

			ptr.next = new List();
			ptr = ptr.next;
		}

		ptr.next = null;
		ptr.work = toadd;
		length++;
	}

	private List head;
	private long length;
	private boolean busy;
	private Job car;
//private Job client;

};

/* This is the queue on which Jobs are placed before they are used. */

class List {

	public List() {
		work = null;
		next = null;
	}

	public SimulationProcess work;
	public List next;

};