# SELFPI Reachability and Tunnel Reconciliation Observation

**Observation ID:** SELFPI-RECONTACT-2026-11-26-02  
**Observed:** 2026-11-26, OURSELFMAC.local  
**State:** MANAGEMENT_PATH_UNRESOLVED / NO_RUNTIME_RECONTACT

## Existing management tunnel inventory

Read-only `cloudflared tunnel info` checks returned no active connections for:

- `SELFPI-MGMT`: `c3409eba-dc57-4e65-83a1-1ea1519aa9ec`
- `SELFPI-OLLAMA`: `90220648-80ab-4e27-af1a-9c9cf321219a`

No tunnel was started, stopped, reconfigured, or repurposed.

## Existing Mac SSH management path

The Mac has a loaded LaunchAgent `com.ourself.selfpi.tunnel` whose SSH command forwards local `127.0.0.1:11435` to remote `127.0.0.1:11434` through SSH alias `ourself-selfpi`.

The alias resolves to hostname `ourselfpimac.local`, user `selfadmin`, port 22. A fresh non-interactive SSH attempt did not establish a session. The name lookup failed from the current Mac network context. The existing LaunchAgent log contains repeated SSH connection timeouts. No remote command executed.

## Distinct voice tunnel origin candidate

The existing local `voice-remote.yml` configuration maps `voice.getsituated.online` to `http://10.0.0.230:49350`. This is a different tunnel configuration and is not evidence that the address is SELFPI.

A read-only reachability probe from OURSELFMAC.local returned:
- ICMP: no reply
- TCP/22: timeout
- TCP/49350: host down
- TCP/11434: host down
- ARP: incomplete

The address is therefore not reachable from the Mac's current network at observation time. No port scan or remote authentication was attempted.

## Interpretation

The current evidence supports only that the two dedicated SELFPI tunnels have no active Cloudflare connections and the Mac's existing SSH route cannot currently establish remote recontact. The voice tunnel's origin address remains an unverified candidate and must not be relabelled as SELFPI without independent identity evidence.

No host identity, runtime identity, storage root, custody, or adapter admission was re-observed. The POSIX adapter remains conformance-tested at D1 only. Canonical memory writes remain unadmitted.

## Next safe operation

Re-establish the SELFPI-MGMT connector from the actual SELFPI host or provide a separately authenticated management ingress. Then verify host/runtime identity and adapter registration read-only before considering any storage operation.
