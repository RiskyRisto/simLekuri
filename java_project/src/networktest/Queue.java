package networktest;


import java.util.NoSuchElementException;

public class Queue {

	public Queue() {
		head = null;
		tail = null;
		length = 0;
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

	public Ship Dequeue() throws NoSuchElementException {
		if (IsEmpty())
			throw (new NoSuchElementException());

		List ptr = head;
		head = head.next;

		length--;
		if (IsEmpty())
			tail = null;

		return ptr.work;
	}

	public void Enqueue(Ship toadd) {
		if (toadd == null)
			return;

		List ptr = head;

		if (IsEmpty()) {
			head = new List();
			ptr = head;
			tail = head;
		} else {
//	    while (ptr.next != null)
//		ptr = ptr.next;
//
//	    ptr.next = new List();
//	    ptr = ptr.next;
			ptr = tail;
			ptr.next = new List();
			tail = ptr.next;
		}

//	ptr.next = null;
//	ptr.work = toadd;
		tail.next = null;
		tail.work = toadd;
		length++;
	}

	private List head;
	private List tail;
	private long length;

};

/* This is the queue on which Jobs are placed before they are used. */

class List {

	public List() {
		work = null;
		next = null;
	}

	public Ship work;
	public List next;

};