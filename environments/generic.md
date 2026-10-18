# Generic environment profile

For an unknown platform:

1. determine whether it is local or cloud-isolated;
2. verify filesystem/shell/Python availability;
3. verify whether the configured AWA Vault is reachable;
4. verify connector/tool/Skill inventory;
5. publish a compact Environment Capability Profile if persistence works;
6. mark uncertain capabilities `UNKNOWN` rather than guessing.
