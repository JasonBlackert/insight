# insight
MQTT Service to Provide 'insight' on Pi's doings

## Local Topics
`insight/$SERIAL/status`
`insight/$SERIAL/cmd`

### Step 0.0 Grab Serial of Device
`cat /sys/firmware/devicetree/base/serial-number`

### Step 1.0 Build
`docker run -u 1000 --rm -itv $PWD:/workspace $(docker build -f insight/Dockerfile -q .) `

### Step 2.0 Copy to Device
`scp insight_0.1.0-1_all.deb target@target-ip:`

### Step 2.1 Install on Target Device
`sudo dpkg -i insight_0.1.0-1_all.deb`

If install doesn't succeed - fix broken
`sudo apt --fix-broken install`
