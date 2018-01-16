# kapacitor-udf-edgedetect
A edgedetection/statechange user defined function in python in a docker container for detecting edges of states in TICKscript  processing streams in the influxdb kapacitor with unix sockets

At present this UDF presumes the selection of string type field


### Constructor 

| Chaining Method | Description |
|:---------|:---------|
| **[edgedetect]()** | Create a node that passes a point only on change of the field selected.  |

### Property Methods

| Setters | Description |
|:---|:---|
| **[field](#as)&nbsp;(&nbsp;`value`&nbsp;`string`)** | The new name of the field to monitor for change of value.  |
| **[as](#as)&nbsp;(&nbsp;`value`&nbsp;`string`)** | The new name of the resulting state field.   |



### Chaining Methods
[Alert](/kapacitor/v1.4/nodes/state_duration_node/#alert), [Bottom](/kapacitor/v1.4/nodes/state_duration_node/#bottom), [Combine](/kapacitor/v1.4/nodes/state_duration_node/#combine), [Count](/kapacitor/v1.4/nodes/state_duration_node/#count), [CumulativeSum](/kapacitor/v1.4/nodes/state_duration_node/#cumulativesum), [Deadman](/kapacitor/v1.4/nodes/state_duration_node/#deadman), ....... TODO: (DESCRIBE MORE)

### Description

Pass as stream point (At this momemnt only string fields will be able to be checked for statechange.) 
If the fields value changes the point that has a different value will be passed through.


Example: 


```javascript
     stream
         |from()
             .measurement('adsl_router')
         |@edgedetect()
             .field('running_state')
             .as('running_state_changes')
             .unit(1m)
         |alert()
             // Warn after 1 minute
             .warn(lambda: "running_state_changes" == '')
             // Critical after 5 minutes
             .crit(lambda: "running_state_changes" == 'TRAINING')
```

Note that as the first point in the given state has no previous point, its 
state will be pressumed static and not passed through.


<a href="javascript:document.getElementsByClassName('article')[0].scrollIntoView();" title="top">^</a>

Properties
----------

Property methods modify state on the calling node.
They do not add another node to the pipeline, and always return a reference to the calling node.
Property methods are marked using the `.` operator.

### Field

The new name of the Field to monitor for edge/state change (AT PRESENT THIS IS only String Fields) 
Default: '......' 


```javascript
@edgedetect.as(value string)
```

<a href="javascript:document.getElementsByClassName('article')[0].scrollIntoView();" title="top">^</a>



### As

The new name of the resulting duration field. 
Default: '......' 


```javascript
@edgedetect.as(value string)
```

<a href="javascript:document.getElementsByClassName('article')[0].scrollIntoView();" title="top">^</a>




Chaining Methods
----------------

Chaining methods create a new node in the pipeline as a child of the calling node.
They do not modify the calling node.
Chaining methods are marked using the `|` operator.


### Alert

Create an alert node, which can trigger alerts. 


```javascript
@edgedetect|alert()
```

Returns: [AlertNode](/kapacitor/v1.4/nodes/alert_node/)

<a href="javascript:document.getElementsByClassName('article')[0].scrollIntoView();" title="top">^</a>

### Further Chaining methods for streams do apply,
TODO: define
