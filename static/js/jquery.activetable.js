	jQuery(function() {
		$('#nextPage,#prevPage').die().live('click', function(){
			var $form = $(this).parents('form');
			var $page = $form.find('#page');
			
			var currentPage = 1;
			
			try {	currentPage = parseInt($page.val()) }
			catch(ex){ currentPage = 1}
			
			if (isNaN( currentPage )) currentPage=1;
			
			if($(this).attr('id')=='nextPage') {
				currentPage++;
				if( $form.find('table tbody tr').length <= 0){currentPage--; return false;}
			} else {
				currentPage--;
				if(currentPage<=0) { currentPage=1; return false}
			}
			
			$page.val(currentPage);
			
			$form.submit();
			return false;
		});
			
			
			
		$('th[sort]').live('click', function(){
			var col = $(this).attr('sort');
			$('#sort').val(col);
			var order = $('#order').val();
			
			$(this).parents('form').find('table thead th i').remove();
			
			if(order=='desc') {
				order='asc';
				$(this).html( $(this).html()  + " <i class='icon-caret-up'></i>");
			} else {
				order='desc';
				$(this).html( $(this).html() + " <i class='icon-caret-down'></i>");
			}
			$('#order').val(order);
			$(this).parents('form').submit();
			return false;
		});
	});