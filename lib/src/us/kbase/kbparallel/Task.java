
package us.kbase.kbparallel;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import us.kbase.common.service.UObject;


/**
 * <p>Original spec-file type: Task</p>
 * <pre>
 * Specifies a task to run.  Parameters is an arbitrary data object
 * passed to the function.  If it is a list, the params will be interpreted
 * as
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "function",
    "params"
})
public class Task {

    /**
     * <p>Original spec-file type: Function</p>
     * <pre>
     * Specifies a specific KBase module function to run
     * </pre>
     * 
     */
    @JsonProperty("function")
    private Function function;
    @JsonProperty("params")
    private UObject params;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
     * <p>Original spec-file type: Function</p>
     * <pre>
     * Specifies a specific KBase module function to run
     * </pre>
     * 
     */
    @JsonProperty("function")
    public Function getFunction() {
        return function;
    }

    /**
     * <p>Original spec-file type: Function</p>
     * <pre>
     * Specifies a specific KBase module function to run
     * </pre>
     * 
     */
    @JsonProperty("function")
    public void setFunction(Function function) {
        this.function = function;
    }

    public Task withFunction(Function function) {
        this.function = function;
        return this;
    }

    @JsonProperty("params")
    public UObject getParams() {
        return params;
    }

    @JsonProperty("params")
    public void setParams(UObject params) {
        this.params = params;
    }

    public Task withParams(UObject params) {
        this.params = params;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((("Task"+" [function=")+ function)+", params=")+ params)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
