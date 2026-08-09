"use client";
import { AnimatePresence, motion } from "framer-motion";
import { useEffect, useState } from "react";
import { connect, EXPLORER, write } from "../lib/chain";
const records = [
  {
    id: "A",
    kind: "PRIMARY",
    title: "Procurement schedule",
    note: "Published 14 JUN",
    x: "16%",
    y: "24%",
  },
  {
    id: "B",
    kind: "PUBLIC DATA",
    title: "Delivery register",
    note: "Updated 30 JUN",
    x: "69%",
    y: "17%",
  },
  {
    id: "C",
    kind: "COUNTERFILE",
    title: "Revision notice",
    note: "Filed 02 JUL",
    x: "73%",
    y: "65%",
  },
  {
    id: "D",
    kind: "FIELD IMAGE",
    title: "South-bank inspection",
    note: "Captured 29 JUN",
    x: "24%",
    y: "72%",
  },
];
function Skeleton() {
  return (
    <main className="loading">
      <div className="orbit">
        <i />
        <i />
        <i />
        <i />
        <b />
      </div>
      <p>TRACING THE PUBLIC RECORD</p>
    </main>
  );
}
export default function Page() {
  const [loading, setLoading] = useState(true),
    [active, setActive] = useState(0),
    [open, setOpen] = useState(false),
    [account, setAccount] = useState(""),
    [claim, setClaim] = useState(""),
    [source, setSource] = useState(""),
    [status, setStatus] = useState(""),
    [hash, setHash] = useState("");
  async function wallet(){try{setAccount(await connect())}catch(e:any){setStatus(e.message)}}
  async function file(){try{await write("file_docket",[`PT-${Date.now()}`,claim,"Municipal works",[source]],(s,h)=>{setStatus(s);if(h)setHash(h)});setOpen(false)}catch(e:any){setStatus(e.message)}}
  useEffect(() => {
    const t = setTimeout(() => setLoading(false), 900);
    return () => clearTimeout(t);
  }, []);
  if (loading) return <Skeleton />;
  const r = records[active];
  return (
    <main>
      <header>
        <a className="mark">
          PT<span>26</span>
        </a>
        <div className="wordmark">
          PUBLIC TRACE<small>AN OPEN EVIDENCE INSTRUMENT</small>
        </div>
        <nav>DOCKET 0241 · BRADBURY</nav>
        <button className="wallet" onClick={wallet}>{account?`${account.slice(0,6)}…${account.slice(-4)}`:"CONNECT ↗"}</button>
      </header>
      <section className="hero">
        <div className="case-no">
          CASE
          <br />
          <b>0241</b>
        </div>
        <motion.h1
          initial={{ opacity: 0, y: 35 }}
          animate={{ opacity: 1, y: 0 }}
        >
          Did the bridge
          <br />
          finish <em>on time?</em>
        </motion.h1>
        <p>
          A public claim is not a verdict. Follow every source, contradiction
          and missing link before the record is sealed.
        </p>
        <button onClick={() => setOpen(true)}>
          FILE A COUNTER-RECORD <span>+</span>
        </button>
        <div className="claimant">
          FILED BY 0x8d14…e203
          <br />
          02 JUL 2026 · MUNICIPAL WORKS
        </div>
      </section>
      <section className="trace">
        <div className="trace-title">
          <span>THE EVIDENCE FIELD</span>
          <small>SELECT A NODE TO INSPECT ITS PLACE IN THE CLAIM</small>
        </div>
        <svg viewBox="0 0 1000 600" preserveAspectRatio="none">
          <path d="M160 145 C360 40 500 100 690 100 S850 220 730 390 C620 540 390 480 240 430 S60 260 160 145" />
          <path d="M160 145 L730 390 M690 100 L240 430" />
        </svg>
        {records.map((x, i) => (
          <motion.button
            whileHover={{ scale: 1.05 }}
            onClick={() => setActive(i)}
            className={`node ${active === i ? "on" : ""}`}
            style={{ left: x.x, top: x.y }}
            key={x.id}
          >
            <i>{x.id}</i>
            <span>{x.kind}</span>
            <b>{x.title}</b>
          </motion.button>
        ))}
        <AnimatePresence mode="wait">
          <motion.article
            key={r.id}
            initial={{ opacity: 0, scale: 0.96 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0 }}
            className="inspector"
          >
            <small>SELECTED / {r.id}</small>
            <h2>{r.title}</h2>
            <p>
              {r.id === "C"
                ? "This notice changes the scope used to define “completed”. It is the unresolved hinge of the claim."
                : "This record independently supports the published sequence of work and remains publicly retrievable."}
            </p>
            <div>
              <span>{r.note}</span>
              <b>{r.id === "C" ? "CONTRADICTS" : "SUPPORTS"}</b>
            </div>
            <a>OPEN ORIGINAL ↗</a>
          </motion.article>
        </AnimatePresence>
        <div className="legend">
          <span>
            <i className="support" />
            SUPPORTS 3
          </span>
          <span>
            <i className="counter" />
            COUNTERS 1
          </span>
          <span>
            <i />
            MISSING 1
          </span>
        </div>
      </section>
      <section className="verdict">
        <small>THE RECORD CURRENTLY LEANS</small>
        <h2>SUBSTANTIALLY TRUE</h2>
        <div className="meter">
          <i />
        </div>
        <p>
          One contractual ambiguity remains. Validators must decide whether the
          revised landscaping scope belonged to the original deadline.
        </p>
        <button>CONVENE PUBLIC REVIEW →</button>
      </section>
      <footer>
        <span>Every line remains inspectable.</span>
        <b>PUBLIC TRACE / GENLAYER</b>
      </footer>
      <AnimatePresence>
        {open && (
          <>
            <motion.div
              className="scrim"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setOpen(false)}
            />
            <motion.div
              className="modal"
              initial={{ y: "100%" }}
              animate={{ y: 0 }}
              exit={{ y: "100%" }}
            >
              <button onClick={() => setOpen(false)}>CLOSE ×</button>
              <small>COUNTER-RECORD / NEW ENTRY</small>
              <h2>Put another fact on the field.</h2>
              <label>
                WHAT DOES THIS RECORD SHOW?
                <textarea value={claim} onChange={e=>setClaim(e.target.value)} placeholder="Write one precise, verifiable observation…" />
              </label>
              <label>
                PUBLIC SOURCE
                <input value={source} onChange={e=>setSource(e.target.value)} placeholder="https://" />
              </label>
              <button className="submit" disabled={claim.length<24||source.length<10} onClick={file}>PLACE ON EVIDENCE FIELD →</button>
            </motion.div>
          </>
        )}
      </AnimatePresence>
      {status&&<div className="chain-status"><b>{status}</b>{hash&&<a href={`${EXPLORER}/${hash}`} target="_blank">VIEW TRANSACTION ↗</a>}<button onClick={()=>setStatus("")}>×</button></div>}
    </main>
  );
}
