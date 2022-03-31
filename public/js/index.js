let app = new Vue({
   el: "#root",
   data() {
      return {
         dataTables: [],
         stdViewer: false,
         stdout: {
            stderr: "",
            stdout: ""
         }
      }
   },
   created() {

   },
   methods: {
      parserSTD(stdout) {
         this.dataTables = [];
         stdout.stdout
          .split("\n\n")
          .filter(e => e.match(/--------------------------------------------------------------------------------/g))
          .map(e =>
              e.replaceAll("\f", "")
               .split("\n\n")
               .map(e => e.split("--------------------------------------------------------------------------------"))
          ).forEach(l1 => {
            l1.forEach(item => {
               let thisTable = {};
               item.forEach((value, index) => {
                  switch (index) {
                     case 0: // title
                        thisTable.title = value.replace(/\n/g, '<br>');
                        thisTable.data = [];
                        break;
                     case 1: // columns
                        value.replaceAll("\n", "").split(" ").filter(e => e != "").forEach(colItem => {
                           thisTable.data.push({
                              columnName: colItem,
                              lists: []
                           });
                        })
                        break;
                     case 2: // lists
                        let thisItem = value.split("\t").filter(e => e != "").map(e => {
                           return e.match(/\-?\d+\.\d+e[+|-]+\d+/g) ? parseFloat(e) + "" : e;
                        })
                        thisItem.forEach((listValue, listIndex) => {
                           thisTable.data[listIndex % thisTable.data.length].lists.push(listValue.replaceAll("\n", ""));
                        })
                        break;
                  }
               })
               this.dataTables.push(thisTable);
            });
         });
      },
      tableMap() {
         let result = [];
         this.dataTables.forEach((item) => {
            let columns = [];
            item.data.forEach((main, indexCol) => {
               main.lists.forEach((value, indexRow) => {
                  let thisColumn = "column" + indexCol;
                  if (columns[indexRow] == undefined) {
                     columns[indexRow] = {};
                  }
                  columns[indexRow][thisColumn] = value;
               })
            })
            result.push(columns);
         })
         return result;
      }
   }
});


/*
    [
        0: {
            title: "...",
            data: [
                {
                    columnName: "...",
                    lists: [
                        "...",
                        "...",
                        "..."
                    ]
                }
            ]
        }
    ]

*/